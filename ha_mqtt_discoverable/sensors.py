#!/usr/bin/env python3
#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import logging

from ha_mqtt_discoverable import Discoverable, SensorInfo

class BinarySensorInfo(SensorInfo):
    """Binary sensor specific information"""
    component: str = "binary_sensor"
    payload_off: str = "on"
    '''Payload to send for the ON state'''
    payload_on: str = "off"
    '''Payload to send for the OFF state'''


class BinarySensor(Discoverable[BinarySensorInfo]):
    
    def off(self):
        """
        Set binary sensor to off
        """
        self._update_state(state=False)

    def on(self):
        """
        Set binary sensor to on
        """
        self._update_state(state=True)

    def _update_state(self, state: bool) -> None:
        """
        Update MQTT device state

        Args:
            state(bool): What state to set the sensor to
        """
        if state:
            state_message = self._sensor.payload_on
        else:
            state_message = self._sensor.payload_off
        logging.info(f"Setting {self._sensor.name} to {state_message} using {self.state_topic}")
        self._state_helper(state=state_message)
