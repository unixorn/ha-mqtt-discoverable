#!/usr/bin/env python3
#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import json
import logging

from ha_mqtt_discoverable import Discoverable, __version__
from ha_mqtt_discoverable.utils import clean_string, valid_configuration_key


class Device(Discoverable):
    def __init__(self, settings: dict = {}) -> None:
        """
        Device initialization

        We will be able to add multiple metrics with

        Device.add_metric()
        """
        super().__init__(settings=settings)
        self.topic_prefix = f"{self.mqtt_prefix}/sensor/{clean_string(self.device_name)}-{clean_string(self.unique_id)}"
        self.config_topic = f"{self.topic_prefix}/config"
        self.state_topic = f"{self.topic_prefix}/state"

        logging.debug(f"device_name: {self.device_name}")
        logging.debug(f"device_id: {self.device_id}")
        logging.debug(f"topic_prefix: {self.topic_prefix}")
        logging.debug(f"self.config_topic: {self.config_topic}")
        logging.debug(f"self.state_topic: {self.state_topic}")
        logging.debug(f"unique_id: {self.unique_id}")

        self.configs = {}
        self.metrics = {}
        self.configured = {}

    def __str__(self) -> str:
        """
        String representation
        """
        base = f"""
{super().__str__()}

metrics: {self.metrics}
configs: {self.configs}
configured: {self.configured}
        """
        return base

    def _device_info(self) -> dict:
        """
        Create a device stanza for the config blob
        """
        device = {
            "name": self.device_name,
            "manufacturer": "Acme Products",
            "sw_version": __version__,
            "identifiers": self.unique_id,
        }
        if hasattr(self, "model"):
            device["model"] = self.model
        if hasattr(self, "manufacturer"):
            device["manufacturer"] = self.manufacturer

        return device

    def add_metric(
        self, name, value, unit_of_measurement: str = "%", configuration: dict = None
    ) -> None:
        """
        Add a metric to our device
        """
        logging.info(f"Adding {name} with {value}")
        self.metrics[name] = value

        if not configuration:
            configuration = {}
            logging.warning(f"No configuration passed in, using {configuration}")

        if "device" not in configuration:
            configuration["device"] = self._device_info()
            logging.warning(f"No device info set, using {configuration['device']}")

        if "object_id" not in configuration:
            configuration["object_id"] = clean_string(f"{name}-{self.unique_id}")
            logging.warning(f"No object_id set, using {configuration['object_id']}")

        if "name" not in configuration:
            configuration["name"] = f"{name} {unit_of_measurement}"
            logging.warning(
                f"Name unset in configuration, using {configuration['name']}"
            )

        if "unit_of_measurement" not in configuration:
            configuration["unit_of_measurement"] = unit_of_measurement
            logging.warning(
                f"No unit_of_measurement set, using {configuration['unit_of_measurement']}"
            )

        if "unique_id" not in configuration:
            configuration["unique_id"] = clean_string(f"{name}_{self.unique_id}")
            logging.warning(f"No unique_id set, using {configuration['unique_id']}")

        name_for_topic = clean_string(name)
        state_topic = f"{self.topic_prefix}/{name_for_topic}/state"
        configuration["state_topic"] = state_topic

        for c in configuration:
            logging.debug(f"checking {c}")
            if not valid_configuration_key(c) and c != "value":
                raise RuntimeError(
                    f"{configuration} contains {c} is not a valid configuration key for a device sensor."
                )

        metric_config = {
            "config_topic": f"{self.topic_prefix}/{name_for_topic}/config",
            "config_message": configuration,
            "state_topic": state_topic,
        }
        logging.debug(f"metric '{name}' using configuration {metric_config}")
        self.configs[name] = metric_config
        self.metrics[name] = value

    def generate_config(self) -> dict:
        config = super().generate_config()
        config["device"] = self._device_info()
        return config

    def write_config(self) -> None:
        """
        Write all the configuration blobs to mqtt
        """
        self._connect()
        logging.debug(f"self.configs: {self.configs}")
        for metric_config in self.configs:
            config_topic = self.configs[metric_config]["config_topic"]
            logging.debug(f"Config topic: {config_topic}")

            config_message = json.dumps(self.configs[metric_config]["config_message"])

            logging.info(
                f"Writing {config_message} to {config_topic} for metric {metric_config}"
            )
            if self.debug:
                logging.debug("Debug mode is {self.debug}, skipping publish")
            else:
                pub = self.mqtt_client.publish(
                    config_topic, config_message, retain=True
                )
                logging.debug(f"state publication results: {pub}")
                self.configured[metric_config] = True

    def write_states(self):
        """
        Write all metrics to their state topics
        """
        self._connect()
        logging.debug(f"self.metrics = {self.metrics}")
        for metric in self.metrics:
            state_topic = self.configs[metric]["state_topic"]
            state = self.metrics[metric]
            logging.debug(f"Writing {state} to {state_topic}")
            if self.debug:
                logging.warning(
                    f"Debug mode is {self.debug}, Skipping state publication"
                )
            else:
                pub = self.mqtt_client.publish(state_topic, state, retain=True)
                logging.debug(f"state publication results: {pub}")

    def publish(self):
        self.write_config()
        self.write_states()
