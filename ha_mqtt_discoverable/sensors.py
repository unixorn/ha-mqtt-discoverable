#
#    Copyright 2022-2024 Joe Block <jpb@unixorn.net>
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

import json
import logging
from typing import Annotated, Any, Literal

from pydantic import Field, model_validator

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
    off_delay: int | None = None
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
    unit_of_measurement: str | None = None
    """Defines the units of measurement of the sensor, if any."""
    state_class: str | None = None
    """Defines the type of state.
    If not None, the sensor is assumed to be numerical
    and will be displayed as a line-chart
    in the frontend instead of as discrete values."""
    value_template: str | None = None
    """
    Defines a template to extract the value.
    If the template throws an error,
    the current state will be used instead."""
    last_reset_value_template: str | None = None
    """
    Defines a template to extract the last_reset.
    When last_reset_value_template is set, the state_class option must be total.
    Available variables: entity_id.
    The entity_id can be used to reference the entity’s attributes."""
    suggested_display_precision: None | Annotated[int, Field(ge=0)] = None
    """
    The number of decimals which should be used in the sensor’s state after rounding.
    """


class SwitchInfo(EntityInfo):
    """Switch specific information"""

    component: str = "switch"
    optimistic: bool | None = None
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
    retain: bool | None = None
    """If the published message should have the retain flag on or not"""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive state updates."""


class LightInfo(EntityInfo):
    """Light specific information"""

    component: str = "light"

    state_schema: str = Field(default="json", alias="schema")  # 'schema' is a reserved word by pydantic
    """Sets the schema of the state topic, ie the 'schema' field in the configuration"""
    optimistic: bool | None = None
    """Flag that defines if light works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_off: str = "OFF"
    """The payload that represents off state. If specified, will be used for
    both comparing to the value in the state_topic (see value_template and
    state_off for details) and sending as off command to the command_topic"""
    payload_on: str = "ON"
    """The payload that represents on state. If specified, will be used for both
    comparing to the value in the state_topic (see value_template and state_on
    for details) and sending as on command to the command_topic."""
    brightness: bool | None = False
    """Flag that defines if the light supports setting the brightness
    """
    color_mode: bool | None = None
    """Flag that defines if the light supports color mode"""
    supported_color_modes: list[str] | None = None
    """List of supported color modes. See
    https://www.home-assistant.io/integrations/light.mqtt/#supported_color_modes for current list of
    supported modes. Required if color_mode is set"""
    effect: bool | None = False
    """Flag that defines if the light supports effects"""
    effect_list: str | list | None = None
    """List of supported effects. Required if effect is set"""
    retain: bool | None = True
    """If the published message should have the retain flag on or not"""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive state updates."""


class CoverInfo(EntityInfo):
    """Cover specific information"""

    component: str = "cover"

    optimistic: bool | None = None
    """Flag that defines if light works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_close: str = "CLOSE"
    """Command payload to close the cover"""
    payload_open: str = "OPEN"
    """Command payload to open the cover"""
    payload_stop: str = "STOP"
    """Command payload to open the cover"""
    position_closed: int = 0
    """Number which represents the fully closed position"""
    position_open: int = 100
    """Number which represents the fully open position"""
    state_open: str = "open"
    """Payload that represents open state"""
    state_opening: str = "opening"
    """Payload that represents opening state"""
    state_closed: str = "closed"
    """Payload that represents closed state"""
    state_closing: str = "closing"
    """Payload that represents closing state"""
    state_stopped: str = "stopped"
    """Payload that represents stopped state"""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive state updates."""
    retain: bool | None = True
    """If the published message should have the retain flag on or not"""


class ButtonInfo(EntityInfo):
    """Button specific information"""

    component: str = "button"

    payload_press: str = "PRESS"
    """The payload to send to trigger the button."""
    retain: bool | None = None
    """If the published message should have the retain flag on or not"""


class TextInfo(EntityInfo):
    """Information about the `text` entity"""

    component: str = "text"

    max: int = 255
    """The maximum size of a text being set or received (maximum is 255)."""
    min: int = 0
    """The minimum size of a text being set or received."""
    mode: str | None = "text"
    """The mode off the text entity. Must be either text or password."""
    pattern: str | None = None
    """A valid regular expression the text being set or received must match with."""

    retain: bool | None = None
    """If the published message should have the retain flag on or not"""


class NumberInfo(EntityInfo):
    """Information about the 'number' entity"""

    component: str = "number"

    max: float | int = 100
    """The maximum value of the number (defaults to 100)"""
    min: float | int = 1
    """The maximum value of the number (defaults to 1)"""
    mode: str | None = None
    """Control how the number should be displayed in the UI. Can be set to box
    or slider to force a display mode."""
    optimistic: bool | None = None
    """Flag that defines if switch works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    payload_reset: str | None = None
    """A special payload that resets the state to None when received on the
    state_topic."""
    retain: bool | None = None
    """If the published message should have the retain flag on or not"""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive state updates."""
    step: float | None = None
    """Step value. Smallest acceptable value is 0.001. Defaults to 1.0."""
    unit_of_measurement: str | None = None
    """Defines the unit of measurement of the sensor, if any. The
    unit_of_measurement can be null."""


class DeviceTriggerInfo(EntityInfo):
    """Information about the device trigger"""

    component: str = "device_automation"
    automation_type: str = "trigger"
    """The type of automation, must be ‘trigger’."""

    payload: str | None = None
    """Optional payload to match the payload being sent over the topic."""
    type: str
    """The type of the trigger"""
    subtype: str
    """The subtype of the trigger"""
    device: DeviceInfo
    """Information about the device this sensor belongs to (required)"""


class CameraInfo(EntityInfo):
    """
    Information about the 'camera' entity.
    """

    component: str = "camera"
    """The component type is 'camera' for this entity."""
    availability_topic: str | None = None
    """The MQTT topic subscribed to publish the camera availability."""
    payload_available: str | None = "online"
    """Payload to publish to indicate the camera is online."""
    payload_not_available: str | None = "offline"
    """Payload to publish to indicate the camera is offline."""
    topic: str | None = None
    """
    The MQTT topic to subscribe to receive an image URL. A url_template option can extract the URL from the message.
    The content_type will be derived from the image when downloaded.
    """
    retain: bool | None = None
    """If the published message should have the retain flag on or not."""


class ImageInfo(EntityInfo):
    """
    Information about the 'image' entity.
    """

    component: str = "image"
    """The component type is 'image' for this entity."""
    availability_topic: str | None = None
    """The MQTT topic subscribed to publish the image availability."""
    payload_available: str | None = "online"
    """Payload to publish to indicate the image is online."""
    payload_not_available: str | None = "offline"
    """Payload to publish to indicate the image is offline."""
    url_topic: str | None = None
    """
    The MQTT topic to subscribe to receive an image URL.
    A url_template option can extract the URL from the message.
    The content_type will be derived from the image when downloaded.
    Cannot be used with image_topic.
    """
    image_topic: str | None = None
    """
    The MQTT topic to subscribe to receive the image payload.
    Cannot be used together with url_topic.
    """
    image_encoding: Literal["b64"] | None = None
    """
    Set the encoding of image payloads when sending images.
    Set to "b64" to enable base64 decoding of image payloads.
    If not set, the image payloads must be raw binary data.
    """
    content_type: str | None = None
    """
    Content type to use when sending image payloads.
    Cannot be used together with url_topic.
    """
    retain: bool | None = None
    """If the published message should have the retain flag on or not."""

    @model_validator(mode="after")
    def image_info_entity_model_validator(self) -> ImageInfo:
        """
        Determine correct usage of configuration variables.
        """
        # Don't set image_topic and url_topic at the same time.
        if self.image_topic and self.url_topic:
            raise ValueError(
                "URL and Image payload sending cannot be used at the same time.Set only one of 'image_topic' or 'url_topic'"
            )

        # Don't set image_encoding and url_topic at the same time.
        if self.image_encoding and self.url_topic:
            raise ValueError("Image encoding should not be set when using url_topic.")

        # Don't set content_type and url_topic at the same time.
        if self.content_type and self.url_topic:
            raise ValueError("Content type should not be set when using url_topic.")

        # Ensure content_type is set if image_topic is used.
        if self.image_topic and not self.content_type:
            raise ValueError("Content type of image payload not set.")

        return self


class SelectInfo(EntityInfo):
    """
    Information about the 'select' entity.
    """

    component: str = "select"
    optimistic: bool | None = None
    """Flag that defines if switch works in optimistic mode.
    Default: true if no state_topic defined, else false."""
    retain: bool | None = None
    """If the published message should have the retain flag on or not"""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive state updates."""
    options: list | None = None
    """List of options that can be selected. An empty list or a list with a single item is allowed."""


class BinarySensor(Discoverable[BinarySensorInfo]):
    def off(self):
        """
        Set binary sensor to off
        """
        self.update_state(state=False)

    def on(self):
        """
        Set binary sensor to on
        """
        self.update_state(state=True)

    def update_state(self, state: bool) -> None:
        """
        Update MQTT sensor state

        Args:
            state(bool): What state to set the sensor to
        """
        state_message = self._entity.payload_on if state else self._entity.payload_off
        logger.info(f"Setting {self._entity.name} to {state_message} using {self.state_topic}")
        self._state_helper(state=state_message)


class Sensor(Discoverable[SensorInfo]):
    def set_state(self, state: str | int | float, last_reset: str = None) -> None:
        """
        Update the sensor state

        Args:
            state(str): What state to set the sensor to
            last_reset(str): ISO 8601-formatted string when an accumulating sensor was initialized
        """
        logger.info(f"Setting {self._entity.name} to {state} using {self.state_topic}")
        if last_reset:
            logger.info("Setting last_reset to " + last_reset)
        self._state_helper(str(state), last_reset=last_reset)


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


class Light(Subscriber[LightInfo]):
    """Implements an MQTT light.
    https://www.home-assistant.io/integrations/light.mqtt
    """

    def on(self) -> None:
        """
        Set light to on
        """
        state_payload = {
            "state": self._entity.payload_on,
        }
        self._update_state(state_payload)

    def off(self) -> None:
        """
        Set light to off
        """
        state_payload = {
            "state": self._entity.payload_off,
        }
        self._update_state(state_payload)

    def brightness(self, brightness: int) -> None:
        """
        Set brightness of the light

        Args:
            brightness(int): Brightness value of [0,255]
        """
        if brightness < 0 or brightness > 255:
            raise RuntimeError(f"Brightness for light {self._entity.name} is out of range")

        state_payload = {
            "brightness": brightness,
            "state": self._entity.payload_on,
        }

        self._update_state(state_payload)

    def color(self, color_mode: str, color: dict[str, Any]) -> None:
        """
        Set color of the light.
        NOTE: Make sure color formatting conforms to color mode, it is up to the caller to make sure
        of this. Also, make sure the color mode is in the list supported_color_modes

        Args:
            color_mode(str): A valid color mode
            color(Dict[str, Any]): Color to set, according to color_mode format
        """
        if not self._entity.color_mode:
            raise RuntimeError(f"Light {self._entity.name} does not support setting color")
        if color_mode not in self._entity.supported_color_modes:
            raise RuntimeError(f"Color is not in configured supported_color_modes {str(self._entity.supported_color_modes)}")
        # We do not check if color schema conforms to color mode formatting, it is up to the caller
        state_payload = {
            "color_mode": color_mode,
            "color": color,
            "state": self._entity.payload_on,
        }
        self._update_state(state_payload)

    def effect(self, effect: str) -> None:
        """
        Enable effect of the light

        Args:
            effect(str): Effect to apply
        """
        if not self._entity.effect:
            raise RuntimeError(f"Light {self._entity.name} does not support effects")
        if effect not in self._entity.effect_list:
            raise RuntimeError(f"Effect is not within configured effect_list {str(self._entity.effect_list)}")
        state_payload = {
            "effect": effect,
            "state": self._entity.payload_on,
        }
        self._update_state(state_payload)

    def _update_state(self, state: dict[str, Any]) -> None:
        """
        Update MQTT sensor state

        Args:
            state(Dict[str, Any]): What state to set the light to
        """
        logger.info(f"Setting {self._entity.name} to {state} using {self.state_topic}")
        json_state = json.dumps(state)
        self._state_helper(state=json_state, topic=self.state_topic, retain=self._entity.retain)


class Cover(Subscriber[CoverInfo]):
    """Implements an MQTT cover:
    https://www.home-assistant.io/integrations/cover.mqtt
    """

    def open(self) -> None:
        """Set cover state to open"""
        self._update_state(self._entity.state_open)

    def closed(self) -> None:
        """Set cover state to closed"""
        self._update_state(self._entity.state_closed)

    def closing(self) -> None:
        """Set cover state to closing"""
        self._update_state(self._entity.state_closing)

    def opening(self) -> None:
        """Set cover state to opening"""
        self._update_state(self._entity.state_opening)

    def stopped(self) -> None:
        """Set cover state to stopped"""
        self._update_state(self._entity.state_stopped)

    def _update_state(self, state: str) -> None:
        """
        Update MQTT sensor state

        Args:
            state(str): What state to set the cover to
        """
        print("State: " + state)
        logger.info(f"Setting {self._entity.name} to {state} using {self.state_topic}")
        self._state_helper(state=state, topic=self.state_topic, retain=self._entity.retain)


class Button(Subscriber[ButtonInfo]):
    """Implements an MQTT button:
    https://www.home-assistant.io/integrations/button.mqtt
    """


class DeviceTrigger(Discoverable[DeviceTriggerInfo]):
    """Implements an MQTT Device Trigger
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

    def trigger(self, payload: str | None = None):
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
            raise RuntimeError(f"Text is not within configured length boundaries {bound}")

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
            value(str): Value of the number configured for this entity
        """
        if not self._entity.min <= value <= self._entity.max:
            bound = f"[{self._entity.min}, {self._entity.max}]"
            raise RuntimeError(f"Value is not within configured boundaries {bound}")

        logger.info(f"Setting {self._entity.name} to {value} using {self.state_topic}")
        self._state_helper(value)


class Camera(Subscriber[CameraInfo]):
    """
    Implements an MQTT camera for Home Assistant MQTT discovery:
    https://www.home-assistant.io/integrations/image.mqtt/
    """

    def set_topic(self, image_topic: str) -> None:
        """
        Update the camera state (image URL).

        Args:
            image_topic (str): Topic of the image to be set as the camera state.
        """
        if not image_topic:
            raise RuntimeError("Image topic cannot be empty")

        logger.info(f"Publishing camera image topic {image_topic} to {self._entity.topic}")
        self._state_helper(image_topic)

    def set_availability(self, available: bool) -> None:
        """
        Update the camera availability status.

        Args:
            available (bool): Whether the camera is available or not.
        """
        payload = self._entity.payload_available if available else self._entity.payload_not_available
        logger.info(f"Setting camera availability to {payload} using {self._entity.availability_topic}")
        self.mqtt_client.publish(self._entity.availability_topic, payload, retain=self._entity.retain)


class Image(Discoverable[ImageInfo]):
    """
    Implements an MQTT image for Home Assistant MQTT discovery:
    https://www.home-assistant.io/integrations/image.mqtt/
    """

    def set_url(self, image_url: str) -> None:
        """
        Update the image URL.

        Args:
            image_url (str): image URL to be published to url_topic.
        """
        if not image_url:
            raise RuntimeError("Image URL cannot be empty")

        logger.info(f"Publishing image URL {image_url} to {self._entity.url_topic}")
        self._state_helper(image_url, self._entity.url_topic)

    def set_payload(self, image_payload: bytes | str) -> None:
        """
        Update the image payload.

        Args:
            image_payload (bytes | str): image payload to be published to image_topic.
        """
        if not image_payload:
            raise RuntimeError("Image payload cannot be empty")

        logger.info(f"Publishing image payload to {self._entity.image_topic}")
        self._state_helper(image_payload, self._entity.image_topic)


class Select(Subscriber[SelectInfo]):
    """
    Implements an MQTT select for Home Assistant MQTT discovery:
    https://www.home-assistant.io/integrations/select.mqtt/
    """

    def select_option(self, option: str) -> None:
        """
        Update the selected option.

        Args:
            option: The option to be selected.
        """
        if not option:
            raise RuntimeError("Option cannot be empty")

        if option not in self._entity.options:
            raise RuntimeError(f"Invalid option: {option} (Valid option(s): {self._entity.options})")

        logger.info(f"Changing selection of {self._entity.name} to {option} using {self.state_topic}")
        self._state_helper(option)
