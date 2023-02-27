import logging
from threading import Event
import time
import pytest

from ha_mqtt_discoverable import EntityInfo, Settings, Subscriber
from paho.mqtt.client import MQTTMessage
import paho.mqtt.publish as publish


@pytest.fixture()
def subscriber() -> Subscriber[EntityInfo]:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="button")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define an empty `command_callback`
    return Subscriber(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="button")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define empty callback
    sensor = Subscriber(settings, lambda *_: None)
    assert sensor is not None


def test_generate_config(subscriber: Subscriber):
    config = subscriber.generate_config()

    assert config is not None
    # Check that command topic is part of the output config
    assert config["command_topic"] == subscriber._command_topic


def test_command_callback():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="switch")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    # Flag that waits for the command to be received
    message_received = Event()

    custom_user_data = "data"

    # Callback to receive the command message
    def custom_callback(client, user_data, message: MQTTMessage):
        payload = message.payload.decode()
        logging.info(f"Received {payload}")
        assert payload == "on"
        assert user_data == custom_user_data
        message_received.set()

    switch = Subscriber(settings, custom_callback, custom_user_data)
    # Wait some seconds for the subscription to take effect
    time.sleep(2)

    # Send a command to the command topic
    publish.single(switch._command_topic, "on", hostname="localhost")

    assert message_received.wait(2)
