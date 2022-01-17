#!.venv/bin/python

import sys
import time
import logging
import json
from os import getenv
from prometheus_client import Gauge, start_http_server
from gpiozero import OutputDevice

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

    

if __name__ == "__main__":
    fan = Fan(gpio_pin=14)
    piaware = PiAware(aircraft_json_path="/run/dump1090-fa/aircraft.json")

    # Expose metrics
    metrics_port = 9200
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))

    while True:
        fan.read_fan_state()
        piaware.read_total_aircraft()
        time.sleep(SLEEP_INTERVAL)
