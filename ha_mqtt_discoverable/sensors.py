#!/usr/bin/env python3
#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import logging

from ha_mqtt_discoverable import Discoverable


class BinarySensor(Discoverable):
    def __init__(self, settings: dict = {}) -> None:
        """
        Binary sensor setup
        """
        self.metric_name = settings["metric_name"]
        super().__init__(settings=settings)
        self.topic_prefix = f"{self.mqtt_prefix}/binary_sensor/{self.device_name}"
        self.config_topic = f"{self.topic_prefix}/config"
        self.state_topic = f"{self.topic_prefix}/state"

        if "payload_off" in settings:
            self.payload_off = settings["payload_off"]
        if "payload_on" in settings:
            self.payload_on = settings["payload_on"]
        if "unique_id" in settings:
            self.unique_id = settings["unique_id"]

        logging.debug(f"metric_name: {self.metric_name}")
        logging.debug(f"topic_prefix: {self.topic_prefix}")
        logging.debug(f"self.state_topic: {self.state_topic}")
        logging.debug(f"settings: {settings}")

    def generate_config(self) -> dict:
        """
        Generate the config blob

        Add device-specific items to the configuration dictionary.
        """
        config = super().generate_config()
        if hasattr(self, "unique_id"):
            config["unique_id"] = self.unique_id
        if hasattr(self, "payload_off"):
            config["payload_off"] = self.payload_off
        if hasattr(self, "payload_on"):
            config["payload_on"] = self.payload_on
        return config

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
        Update MQTT device state

        Args:
            state(bool): What state to set the sensor to
        """
        if state:
            state_message = "ON"
        else:
            state_message = "OFF"
        logging.info(
            f"Setting {self.device_name} to {state_message} using {self.state_topic}"
        )
        self._state_helper(state=state_message)
