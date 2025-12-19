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
import logging
import random
import string
import time
from collections.abc import Callable
from threading import Event
from typing import Any, TypeVar

import paho.mqtt.client as mqtt
import pytest
from paho.mqtt import publish
from paho.mqtt.client import MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion

from ha_mqtt_discoverable import EntityInfo, Settings, Subscriber

T = TypeVar("T")  # Used in the callback function


@pytest.fixture
def make_subscriber():
    def _make_subscriber(
        callback: Callable[[mqtt.Client, T, mqtt.MQTTMessage], Any] = lambda _, __, ___: None,
        mqtt_client: mqtt.Client | None = None,
    ):
        mqtt_settings = Settings.MQTT(client=mqtt_client) if mqtt_client else Settings.MQTT(host="localhost")
        sensor_info = EntityInfo(name="".join(random.choices(string.ascii_lowercase + string.digits, k=10)), component="button")
        settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
        return Subscriber(settings, callback)

    return _make_subscriber


@pytest.fixture
def subscriber(make_subscriber) -> Subscriber[EntityInfo]:
    return make_subscriber()


def test_required_config(subscriber: Subscriber):
    assert subscriber is not None


def test_generate_config(subscriber: Subscriber):
    config = subscriber.generate_config()

    assert config is not None
    # Check that command topic is part of the output config
    assert config["command_topic"] == subscriber._command_topic


def create_callback(event: Event, expected_payload: str) -> Callable:
    # Callback to receive the command message
    def custom_callback(_, user_data, message: MQTTMessage):
        payload = message.payload.decode()
        logging.info(f"Received {payload}")
        assert payload == expected_payload
        assert user_data is None
        event.set()

    return custom_callback


def create_external_mqtt_client() -> mqtt.Client:
    mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    mqtt_client.connect(host="localhost")
    mqtt_client.loop_start()
    return mqtt_client


@pytest.mark.parametrize("mqtt_client", [None, create_external_mqtt_client()])
def test_command_callbacks(make_subscriber, mqtt_client):
    # Flag that waits for the command to be received
    event1 = Event()
    event2 = Event()
    expected_payload1 = "on"
    expected_payload2 = "off"
    custom_callback1 = create_callback(event1, expected_payload1)
    custom_callback2 = create_callback(event2, expected_payload2)
    subscriber1 = make_subscriber(custom_callback1, mqtt_client)
    subscriber2 = make_subscriber(custom_callback2, mqtt_client)
    # Wait for the subscription to take effect
    time.sleep(1)

    assert subscriber1._command_topic != subscriber2._command_topic

    # Send a command to the command topic
    publish.single(subscriber1._command_topic, expected_payload1)
    publish.single(subscriber2._command_topic, expected_payload2)

    assert event1.wait(1)
    assert event2.wait(1)


def test_expect_exception_if_subscribing_the_command_topic_fails(make_subscriber):
    mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    # MQTT client is _not_ connected to the broker
    with pytest.raises(RuntimeError, match="Error subscribing to MQTT command topic"):
        make_subscriber(lambda _, __, ___: None, mqtt_client)
