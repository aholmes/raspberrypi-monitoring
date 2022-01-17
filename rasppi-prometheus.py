#!.venv/bin/python

import sys
import time
import logging
import json
import re
from os import getenv
from prometheus_client import Gauge, start_http_server
from gpiozero import OutputDevice
from dotenv import dotenv_values
sys.path.insert(1, "/usr/share/weather-util")
import weather

logging.basicConfig(level=getenv("LOGLEVEL") or logging.ERROR)
log = logging.getLogger()

SLEEP_INTERVAL = 1

class Fan:
    _gauge: Gauge
    _fan: OutputDevice

    def __init__(self, gpio_pin: int):
        self._gauge = Gauge("fan", "Fan", ["state"])
        self._fan = OutputDevice(gpio_pin)
        self._set_gauge_state(0)

    def _set_gauge_state(self, state: int):
        self._gauge.labels("state").set(state)

    def read_fan_state(self):
        state = self._fan.value
        log.info(f"Fan state is: {state}")
        self._set_gauge_state(state)

class PiAware:
    _gauge: Gauge
    _aircraft_json_path: str

    def __init__(self, aircraft_json_path: str):
        self._gauge = Gauge("aircraft", "Aircraft", ["total"])
        self._aircraft_json_path = aircraft_json_path
        self._set_gauge_total(0)

    def _set_gauge_total(self, total: int):
        self._gauge.labels("total").set(total)

    def read_total_aircraft(self):
        with open(self._aircraft_json_path) as aircraft_json:
            aircraft = json.load(aircraft_json)
            total_aircraft = len(aircraft["aircraft"])
            log.info(f"Aircraft total is: {total_aircraft}")
            self._set_gauge_total(total_aircraft)

class PiAwareWeather:
    """
    Assumes PiAware is installed so it can source location.env.
    Assumes `weather-util` is installed.
    """

    _gauge: Gauge
    _weather_argument: str
    _weather_selections: weather.Selections

    _re_temperature = re.compile(r"^\s+Temperature: ([0-9]+\.[0-9]) F", re.MULTILINE)
    _re_humidity = re.compile(r"^\s+Relative Humidity: ([0-9]+)%", re.MULTILINE)
    _re_winddirection = re.compile(r"^\s+Wind:.+\(([0-9]+) degrees\)", re.MULTILINE)
    _re_windspeed = re.compile(r"^\s+Wind:.+ at ([0-9]+) MPH", re.MULTILINE)
    _re_conditions = re.compile(r"^\s+Sky conditions: (.+)$", re.MULTILINE)

    def __init__(self):
        self._gauge = Gauge("weather", "Weather", ["metric"])
        location_config = dotenv_values("/var/cache/piaware/location.env")
        latitude = location_config['PIAWARE_LAT']
        longitude = location_config['PIAWARE_LON']
        self._weather_argument = f"{latitude},{longitude}"
        self._weather_selections = weather.Selections()

    def _set_gauge(self,
        temperature: float,
        humidity: int,
        winddirection: int,
        windspeed: int,
        conditions: str
    ):
        self._gauge.labels(metric="temperature").set(temperature)
        self._gauge.labels(metric="humidity").set(humidity)
        self._gauge.labels(metric="winddirection").set(winddirection)
        self._gauge.labels(metric="windspeed").set(windspeed)
        self._gauge.labels(metric="conditions").set(0) # TODO this will need to be an enum as prometheus expects numeric metric values

    def read_weather(self):
        argument = self._weather_argument
        selections = self._weather_selections

        metar = weather.get_metar(
            uri=selections.get("metar", argument),
            verbose=selections.get_bool("verbose", argument),
            quiet=selections.get_bool("quiet", argument),
            headers=selections.get("headers", argument),
            imperial=selections.get_bool("imperial", argument),
            metric=selections.get_bool("metric", argument),
            cache_data=(
                selections.get_bool("cache") \
                    and selections.get_bool("cache_data")
            ),
            cacheage=selections.getint("cacheage"),
            cachedir=selections.get("cachedir")
        ).strip()
        
        self._set_gauge(
            self._re_temperature.findall(metar)[0],
            self._re_humidity.findall(metar)[0],
            self._re_winddirection.findall(metar)[0],
            self._re_windspeed.findall(metar)[0],
            self._re_conditions.findall(metar)[0]
        )

    

if __name__ == "__main__":
    fan = Fan(gpio_pin=14)
    piaware = PiAware(aircraft_json_path="/run/dump1090-fa/aircraft.json")
    piaware_weather = PiAwareWeather()

    piaware_weather.read_weather()

    # Expose metrics
    metrics_port = 9200
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))

    while True:
        fan.read_fan_state()
        piaware.read_total_aircraft()
        piaware_weather.read_weather()
        time.sleep(SLEEP_INTERVAL)
