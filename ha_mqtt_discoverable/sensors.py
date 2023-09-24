#
#    Copyright 2022-2023 Joe Block <jpb@unixorn.net>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Required to define a class itself as type https://stackoverflow.com/a/33533514
from __future__ import annotations

import logging
from typing import Any, Optional

from ha_mqtt_discoverable import (
    DeviceInfo,
    Discoverable,
    EntityInfo,
    Subscriber,
)

logger = logging.getLogger(__name__)


class BinarySensorInfo(EntityInfo):
    """Binary sensor specific information"""

    component: str = "binary_sensor"
    off_delay: Optional[int] = None
    """For sensors that only send on state updates (like PIRs), this variable
    sets a delay in seconds after which the sensor's state will be updated back
    to off."""
    payload_off: str = "off"
    """Payload to send for the ON state"""
    payload_on: str = "on"
    """Payload to send for the OFF state"""


class SensorInfo(EntityInfo):
    """Sensor specific information"""

    component: str = "sensor"
    unit_of_measurement: Optional[str] = None
    """Defines the units of measurement of the sensor, if any."""
    state_class: Optional[str] = None
    """Defines the type of state.
    If not None, the sensor is assumed to be numerical
    and will be displayed as a line-chart
    in the frontend instead of as discrete values."""


class SwitchInfo(EntityInfo):
    """Switch specific information"""

    component: str = "switch"
    optimistic: Optional[bool] = None
    """Flag that defines if switch works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_off: str = "OFF"
    """The payload that represents off state. If specified, will be used for
    both comparing to the value in the state_topic (see value_template and
    state_off for details) and sending as off command to the command_topic"""
    payload_on: str = "ON"
    """The payload that represents on state. If specified, will be used for both
    comparing to the value in the state_topic (see value_template and state_on
    for details) and sending as on command to the command_topic."""
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


class TextInfo(EntityInfo):
    """Information about the `text` entity"""

    component: str = "text"

    max: int = 255
    """The maximum size of a text being set or received (maximum is 255)."""
    min: int = 0
    """The minimum size of a text being set or received."""
    mode: Optional[str] = "text"
    """The mode off the text entity. Must be either text or password."""
    pattern: Optional[str] = None
    """A valid regular expression the text being set or received must match with."""

    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""


class NumberInfo(EntityInfo):
    """Information about the 'number' entity"""

    component: str = "number"

    max: float | int = 100
    """The maximum value of the number (defaults to 100)"""
    min: float | int = 1
    """The maximum value of the number (defaults to 1)"""
    mode: Optional[str] = None
    """Control how the number should be displayed in the UI. Can be set to box
    or slider to force a display mode."""
    optimistic: Optional[bool] = None
    """Flag that defines if switch works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_reset: Optional[str] = None
    """A special payload that resets the state to None when received on the
    state_topic."""
    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""
    state_topic: Optional[str] = None
    """The MQTT topic subscribed to receive state updates."""
    step: Optional[float] = None
    """Step value. Smallest acceptable value is 0.001. Defaults to 1.0."""
    unit_of_measurement: Optional[str] = None
    """Defines the unit of measurement of the sensor, if any. The
    unit_of_measurement can be null."""


class DeviceTriggerInfo(EntityInfo):
    """Information about the device trigger"""

    component: str = "device_automation"
    automation_type: str = "trigger"
    """The type of automation, must be ‘trigger’."""

    payload: Optional[str] = None
    """Optional payload to match the payload being sent over the topic."""
    type: str
    """The type of the trigger"""
    subtype: str
    """The subtype of the trigger"""
    device: DeviceInfo
    """Information about the device this sensor belongs to (required)"""


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
        logger.info(
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
        logger.info(f"Setting {self._entity.name} to {state} using {self.state_topic}")
        self._state_helper(str(state))


# Inherit the on and off methods from the BinarySensor class, changing only the
# documentation string
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


class DeviceTrigger(Discoverable[DeviceTriggerInfo]):
    """Implements an MWTT Device Trigger
    https://www.home-assistant.io/integrations/device_trigger.mqtt/
    """

    def generate_config(self) -> dict[str, Any]:
        """Publish a custom configuration: since this entity does not provide a
        `state_topic`, HA expects a `topic` key in the config
        """
        config = super().generate_config()
        # Publish our `state_topic` as `topic`
        topics = {
            "topic": self.state_topic,
        }
        return config | topics

    def trigger(self, payload: Optional[str] = None):
        """
        Generate a device trigger event

        Args:
            payload: custom payload to send in the trigger topic

        """
        return self._state_helper(payload, self.state_topic, retain=False)


class Text(Subscriber[TextInfo]):
    """Implements an MQTT text:
    https://www.home-assistant.io/integrations/text.mqtt/
    """

    def set_text(self, text: str) -> None:
        """
        Update the text displayed by this sensor. Check that it is of acceptable length.

        Args:
            text(str): Value of the text configured for this entity
        """
        if not self._entity.min <= len(text) <= self._entity.max:
            bound = f"[{self._entity.min}, {self._entity.max}]"
            raise RuntimeError(
                f"Text is not within configured length boundaries {bound}"
            )

        logger.info(f"Setting {self._entity.name} to {text} using {self.state_topic}")
        self._state_helper(str(text))


class Number(Subscriber[NumberInfo]):
    """Implements an MQTT number:
    https://www.home-assistant.io/integrations/number.mqtt/
    """

    def set_value(self, value: float) -> None:
        """
        Update the numeric value. Raises an error if not within the acceptable range.

        Args:
            text(str): Value of the text configured for this entity
        """
        if not self._entity.min <= value <= self._entity.max:
            bound = f"[{self._entity.min}, {self._entity.max}]"
            raise RuntimeError(f"Value is not within configured boundaries {bound}")

        logger.info(f"Setting {self._entity.name} to {value} using {self.state_topic}")
        self._state_helper(value)
