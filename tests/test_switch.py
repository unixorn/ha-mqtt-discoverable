import logging
from threading import Event
import time
import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo
from paho.mqtt.publish import single
from paho.mqtt.client import MQTTMessage


@pytest.fixture(name="sensor")
def switch() -> Switch:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test", command_topic="command")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Switch(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Switch(settings)
    assert sensor is not None


def test_generate_config(sensor: Switch):
    config = sensor.generate_config()

    assert config is not None
    # If we have defined a command topic, check that is part of the output config
    assert config["command_topic"] == sensor._entity.command_topic


def test_set_callback(sensor: Switch):
    message_received = Event()
    sensor.write_config()

    # Callback to receive the command message
    def callback(client, userdata, message: MQTTMessage):
        payload = message.payload.decode()
        logging.info(f"Received {payload}")
        assert payload == "on"
        message_received.set()

    sensor.set_callback(callback)
    # Wait some seconds for the subscription to take effect
    time.sleep(2)

    # Send a command to the command topic
    single(sensor._command_topic, "on", hostname="localhost")

    assert message_received.wait(1)
