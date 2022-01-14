#!.venv/bin/python

import sys
import time
import logging
from prometheus_client import Gauge, start_http_server
from gpiozero import OutputDevice

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

SLEEP_INTERVAL = 1
GPIO_PIN = 14

class Fan:
    _gauge: Gauge
    _fan: OutputDevice

    def __init__(self, gpio_pin):
        self._gauge = Gauge('fan', 'Fan', ['state'])
        self._fan = OutputDevice(gpio_pin)
        self._set_gauge_state(0)

    def _set_gauge_state(self, state):
        self._gauge.labels('state').set(state)

    def read_fan_state(self):
        state = self._fan.value
        log.info(f'Fan state is: {state}')
        self._set_gauge_state(state)


if __name__ == "__main__":
    fan = Fan(GPIO_PIN)
    # Expose metrics
    metrics_port = 9200
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))

    while True:
        fan.read_fan_state()
        time.sleep(SLEEP_INTERVAL)
