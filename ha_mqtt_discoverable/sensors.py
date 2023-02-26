#!/usr/bin/env python3
#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0
from __future__ import annotations  # Required to define a class itself as type https://stackoverflow.com/a/33533514
import logging
from typing import Any, Callable, Optional, TypeVar
from paho.mqtt.client import Client, MQTTMessage, MQTT_ERR_SUCCESS
from ha_mqtt_discoverable import Discoverable, EntityInfo, Settings


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


class Switch(Discoverable[SwitchInfo]):
    T = TypeVar("T")  # Used in the callback function
    _command_topic: str

    def __init__(self, settings: Settings[SwitchInfo]) -> None:
        super().__init__(settings)
        self._command_topic = f"{self._discovery_topic_prefix}/command"

    def off(self):
        """
        Set switch to off
        """
        self._update_state(state=False)

    def on(self):
        """
        Set switch to on
        """
        self._update_state(state=True)

    def set_callback(self, callback: Callable[[Client, T, MQTTMessage], Any], user_data: T = None):
        """
        Define a callback function that is invoked when Home Assistant request to change the state of this switch.
        If defined, the `user_data` parameter is passed back to the callback function
        """
        # Callback invoked when the connection is established
        def on_connect(client: Client, *args):
            # Publish this button in Home Assistant
            self.write_config()
            # Subscribe to the command topic
            result, _ = client.subscribe(self._command_topic, qos=1)
            if result is not MQTT_ERR_SUCCESS:
                raise RuntimeError("Error subscribing to MQTT command topic")

        self.mqtt_client.on_message = callback
        self.mqtt_client.user_data_set(user_data)
        # When the connection is established start the subscription
        self.mqtt_client.on_connect = on_connect

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

    def generate_config(self) -> dict[str, Any]:
        """Override base config to add the command topic of this switch"""
        config = super().generate_config()
        # Add the MQTT command topic to the existing config object
        topics = {
            "command_topic": self._command_topic,
        }
        return config | topics


class Button(Discoverable[ButtonInfo]):
    """
    https://www.home-assistant.io/integrations/button.mqtt
    """
    T = TypeVar("T")  # Used in the callback function
    _command_topic: str

    def __init__(self, settings: Settings[ButtonInfo]) -> None:
        super().__init__(settings)
        self._command_topic = f"{self._discovery_topic_prefix}/command"

    def set_callback(self, callback: Callable[[Client, T, MQTTMessage], Any], user_data: T = None):
        """
        Define a callback function that is invoked when Home Assistant request a press of this button.
        If defined, the `user_data` parameter is passed back to the callback function
        """
        # Callback invoked when the connection is established
        def on_connect(client: Client, *args):
            # Publish this button in Home Assistant
            self.write_config()
            # Subscribe to the command topic
            result, _ = client.subscribe(self._command_topic, qos=1)
            if result is not MQTT_ERR_SUCCESS:
                raise RuntimeError("Error subscribing to MQTT command topic")

        self.mqtt_client.on_message = callback
        self.mqtt_client.user_data_set(user_data)
        # When the connection is established start the subscription
        self.mqtt_client.on_connect = on_connect

    def generate_config(self) -> dict[str, Any]:
        """Override base config to add the command topic of this button"""
        config = super().generate_config()
        # Add the MQTT command topic to the existing config object
        topics = {
            "command_topic": self._command_topic,
        }
        return config | topics

