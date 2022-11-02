# Copyright 2022 Joe Block <jpb@unixorn.net>
#
# License: Apache 2.0 (see root of the repo)

import json
import logging

import paho.mqtt.client as mqtt


class Discoverable:
    """
    Base class for making MQTT discoverable objects
    """

    def __init__(self, settings: dict = {}) -> None:
        """
        Validate the settings and setup the base discoverable object class

        Args:
            settings(dict): Settings for the sensor we want to create in Home Assistant.

            Mandatory Keys:
                mqtt_server
                mqtt_prefix - defaults to homeassistant
                mqtt_user
                mqtt_password
                device_id
                device_name
                device_class

            Optional Keys:
                payload_off
                payload_on
                unique_id
        """
        logging.warning("In Discoverable __init__")
        settings_error_base = f"You must specify a server and a client_name"

        assert "client_name" in settings, f"client_name is unset. {settings_error_base}"
        self.client_name = settings["client_name"]

        assert "mqtt_server" in settings, f"mqtt_server is unset. {settings_error_base}"
        self.mqtt_server = settings["mqtt_server"]

        assert "mqtt_prefix" in settings, f"mqtt_prefix is unset. {settings_error_base}"
        self.mqtt_prefix = settings["mqtt_prefix"]

        assert (
            "mqtt_password" in settings
        ), f"mqtt_password is unset. {settings_error_base}"
        self.mqtt_password = settings["mqtt_password"]

        assert "mqtt_user" in settings, f"mqtt_user is unset. {settings_error_base}"
        self.mqtt_user = settings["mqtt_user"]

        assert "device_id" in settings, f"device_id is unset. {settings_error_base}"
        self.device_id = settings["device_id"]

        assert "device_name" in settings, f"device_name is unset. {settings_error_base}"
        self.device_name = settings["device_name"]

        assert (
            "device_class" in settings
        ), f"device_class is unset. {settings_error_base}"
        self.device_class = settings["device_class"]

        self.topic_prefix = f"{self.mqtt_prefix}/{self.device_class}/{self.device_name}"
        self.config_topic = f"{self.topic_prefix}/config"
        self.state_topic = f"{self.topic_prefix}/state"
        logging.info(f"topic_prefix: {self.topic_prefix}")
        logging.info(f"self.state_topic: {self.state_topic}")
        self.wrote_configuration = False
        logging.warning("Finishing Discoverable __init__")

    def _connect(self) -> None:
        logging.debug(
            f"Creating mqtt client({self.client_name}) for {self.mqtt_server}"
        )
        self.mqtt_client = mqtt.Client(self.client_name)

        logging.info(f"Connecting to {self.mqtt_server}...")
        self.mqtt_client.connect(self.mqtt_server)

    def _state_helper(self, state: str = None, topic: str = None) -> None:
        """
        Write a state to our MQTT state topic
        """
        if not hasattr(self, "mqtt_client"):
            logging.warning(f"Connecting to {self.mqtt_server}...")
            self._connect()
        if not self.wrote_configuration:
            logging.debug(f"Writing sensor configuration")
            self.write_config()
        if not topic:
            logging.debug(f"topic unset, using default of '{self.state_topic}'")
            topic = self.state_topic
        logging.debug(f"Writing '{state}' to {topic}")
        logging.warning(self.mqtt_client.publish(topic, state, retain=True))

    def delete(self) -> None:
        """
        Delete a synthetic sensor from Home Assistant via MQTT message.

        Based on https://www.home-assistant.io/docs/mqtt/discovery/
        mosquitto_pub -r -h 127.0.0.1 -p 1883 -t "homeassistant/binary_sensor/garden/config" \
            -m '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}'
        """

        config_message = ""

        logging.info(
            f"Writing '{config_message}' to topic {self.config_topic} on {self.mqtt_server}"
        )
        self.mqtt_client.publish(self.config_topic, config_message, retain=True)

    def generate_config(self) -> dict:
        """
        Generate a dictionary that we'll grind into JSON and write to MQTT.

        Will be used with the MQTT discovery protocol to make Home Assistant
        automagically ingest the new sensor.
        """
        config = {
            "name": self.device_name,
            "device_class": self.device_class,
            "state_topic": self.state_topic,
        }
        return config

    def write_config(self) -> None:
        """
        mosquitto_pub -r -h 127.0.0.1 -p 1883 -t "homeassistant/binary_sensor/garden/config" \
            -m '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}'
        """

        config_message = json.dumps(self.generate_config())

        logging.debug(
            f"Writing '{config_message}' to topic {self.config_topic} on {self.mqtt_server}"
        )
        self.wrote_configuration = True
        if not hasattr(self, "mqtt_client"):
            logging.info(f"Connecting to {self.mqtt_server}...")
            self._connect()
        else:
            logging.debug("mqtt_client already set")
        self.mqtt_client.publish(self.config_topic, config_message, retain=True)

    def update_state(self, state) -> None:
        """
        Update MQTT device state

        Override in subclasses
        """
        self._state_helper(state=state)
