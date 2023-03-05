#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0
# Required to define a class itself as type https://stackoverflow.com/a/33533514
from __future__ import annotations
import logging
from typing import Optional
from ha_mqtt_discoverable import Discoverable, EntityInfo, Subscriber


class BinarySensorInfo(EntityInfo):
    """Binary sensor specific information"""

    component: str = "binary_sensor"
    off_delay: Optional[int] = None
    """For sensors that only send on state updates (like PIRs),
    this variable sets a delay in seconds after which the sensor’s state will be updated back to off."""
    payload_off: str = "on"
    """Payload to send for the ON state"""
    payload_on: str = "off"
    """Payload to send for the OFF state"""


class SensorInfo(EntityInfo):
    """Sensor specific information"""

    component: str = "sensor"
    unit_of_measurement: Optional[str] = None
    """Defines the units of measurement of the sensor, if any."""


class SwitchInfo(EntityInfo):
    """Switch specific information"""

    component: str = "switch"
    optimistic: Optional[bool] = None
    """Flag that defines if switch works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_off: str = "OFF"
    """The payload that represents off state. If specified, will be used for both comparing
    to the value in the state_topic (see value_template and state_off for details)
    and sending as off command to the command_topic"""
    payload_on: str = "ON"
    """The payload that represents on state. If specified, will be used for both comparing
     to the value in the state_topic (see value_template and state_on for details)
     and sending as on command to the command_topic."""
    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""
    state_topic: Optional[str] = None
    """The MQTT topic subscribed to receive state updates."""


class ButtonInfo(EntityInfo):
    """Button specific information"""

    component: str = "button"

    payload_press: str = "PRESS"
    """The payload to send to trigger the button."""
    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""


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
        Update MQTT sensor state

        Args:
            state(bool): What state to set the sensor to
        """
        if state:
            state_message = self._entity.payload_on
        else:
            state_message = self._entity.payload_off
        logging.info(
            f"Setting {self._entity.name} to {state_message} using {self.state_topic}"
        )
        self._state_helper(state=state_message)


class Sensor(Discoverable[SensorInfo]):
    def set_state(self, state: str | int | float) -> None:
        """
        Update the sensor state

        Args:
            state(str): What state to set the sensor to
        """
        logging.info(f"Setting {self._entity.name} to {state} using {self.state_topic}")
        self._state_helper(str(state))


# Inherit the on and off methods from the BinarySensor class, changing only the documentation string
class Switch(Subscriber[SwitchInfo], BinarySensor):
    """Implements an MQTT switch:
    https://www.home-assistant.io/integrations/switch.mqtt
    """

    def off(self):
        """
        Set switch to off
        """
        super().off()

    def on(self):
        """
        Set switch to on
        """
        super().on()


class Button(Subscriber[ButtonInfo]):
    """Implements an MQTT button:
    https://www.home-assistant.io/integrations/button.mqtt
    """
