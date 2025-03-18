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
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from unittest.mock import MagicMock

import pytest
from paho.mqtt import subscribe
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
    Client,
    MQTTMessage,
    MQTTv5,
)
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.subscribeoptions import SubscribeOptions
from pytest_mock import MockerFixture

from ha_mqtt_discoverable import DeviceInfo, Discoverable, EntityInfo, Settings


@pytest.fixture
def discoverable() -> Discoverable[EntityInfo]:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Discoverable[EntityInfo](settings)


@pytest.fixture
def discoverable_availability() -> Discoverable[EntityInfo]:
    """Return an instance of Discoverable configured with `manual_availability`"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info, manual_availability=True)
    return Discoverable[EntityInfo](settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable(settings)
    assert d is not None


def test_missing_config():
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    # Missing MQTT settings
    with pytest.raises(ValueError):
        Settings(entity=sensor_info)  # type: ignore


def test_custom_on_connect():
    """Test that the custom callback function is invoked when we connect to MQTT"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    is_connected = Event()

    def custom_callback(*args):
        is_connected.set()
        pass

    d = Discoverable(settings, custom_callback)
    d._connect_client()
    assert is_connected.wait(5)


def test_custom_on_connect_must_be_called(mocker: MockerFixture):
    """Test that _on_connect must be called if there is a custom_callback"""
    mocked_client = mocker.patch("paho.mqtt.client.Client")
    mock_instance: MagicMock = mocked_client.return_value

    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    # Define an empty lambda callback
    Discoverable(settings, lambda: None)
    # Avoid calling d._connect_client()
    # Verify that on_connect on the client was not called
    mock_instance.assert_not_called()


def test_mqtt_topics():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    assert d._entity_topic == "binary_sensor/test"
    assert d.config_topic == "homeassistant/binary_sensor/test/config"
    assert d.state_topic == "hmd/binary_sensor/test/state"
    assert d.attributes_topic == "hmd/binary_sensor/test/attributes"


def test_mqtt_topics_with_device():
    mqtt_settings = Settings.MQTT(host="localhost")
    device = DeviceInfo(name="test_device", identifiers="id")
    sensor_info = EntityInfo(name="test", component="binary_sensor", device=device, unique_id="unique_id")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    assert d._entity_topic == "binary_sensor/test_device/test"
    assert d.config_topic == "homeassistant/binary_sensor/test_device/test/config"
    assert d.state_topic == "hmd/binary_sensor/test_device/test/state"
    assert d.attributes_topic == "hmd/binary_sensor/test_device/test/attributes"


def test_generate_config(discoverable: Discoverable):
    device_config = discoverable.generate_config()

    assert device_config is not None
    assert device_config["name"] == "test"
    assert device_config["component"] == "binary_sensor"
    assert device_config["state_topic"] == "hmd/binary_sensor/test/state"
    assert device_config["json_attributes_topic"] == "hmd/binary_sensor/test/attributes"


def test_setup_client(discoverable: Discoverable):
    # Try to setup client
    discoverable._setup_client()
    # Check that we save the client
    assert discoverable.mqtt_client is not None


def test_connect_client(discoverable: Discoverable):
    # Try to connect to MQTT
    discoverable._setup_client()
    discoverable._connect_client()
    # Check that we save the client
    assert discoverable.mqtt_client is not None


def test_write_config(discoverable: Discoverable):
    # Write config to MQTT
    discoverable.write_config()

    assert discoverable.wrote_configuration is True
    assert discoverable.config_message is not None


def test_state_helper(discoverable: Discoverable):
    # Write a state to MQTT
    discoverable._state_helper("test")
    # Check that flag is set
    assert discoverable.wrote_configuration is True
    assert discoverable.config_message is not None


def test_device_info(discoverable: Discoverable[EntityInfo]):
    device_info = DeviceInfo(name="Test device", identifiers="test_device_id")
    # Assign the sensor to a device
    discoverable._entity.device = device_info
    discoverable._entity.unique_id = "test_sensor"
    config = discoverable.generate_config()

    # Check that the device info is put in the output config
    assert config["device"] is not None
    assert config["device"]["name"] == "Test device"

    discoverable.write_config()


def test_device_missing_unique_id():
    device_info = DeviceInfo(name="Test device", identifiers="test_device_id")
    with pytest.raises(ValueError):
        EntityInfo(name="test", component="binary_sensor", device=device_info)


def test_device_without_identifiers():
    # Identifiers or connections is required
    with pytest.raises(ValueError):
        DeviceInfo(name="Test device")


def test_device_with_unique_id():
    device_info = DeviceInfo(name="Test device", identifiers="test_device_id")
    EntityInfo(name="test", component="binary_sensor", unique_id="id", device=device_info)


def test_name_with_space():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="Name with space", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    d.write_config()


def test_custom_object_id():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="Test name", component="binary_sensor", object_id="custom object id")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    d.write_config()


def test_str(discoverable: Discoverable[EntityInfo]):
    string = str(discoverable)
    print(string)
    assert "settings" in string


# Define a callback function to be invoked when we receive a message on the topic
def message_callback(client: Client, userdata, message: MQTTMessage, tmp=None):
    logging.info("Received %s", message)
    # If the broker is `dirty` and contains messages send by other test functions,
    # skip these retained messages
    if message.retain:
        logging.warn("Skipping retained message")
        return
    payload = message.payload.decode()
    assert "test" in payload
    userdata.set()
    client.disconnect()


def test_publish_multithread(discoverable: Discoverable):
    received_message = Event()
    mqtt_client = Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5, userdata=received_message)

    mqtt_client.connect(host="localhost")
    mqtt_client.on_message = message_callback
    mqtt_client.subscribe(
        (
            "hmd/binary_sensor/test/state/#",
            SubscribeOptions(retainHandling=SubscribeOptions.RETAIN_DO_NOT_SEND),
        )
    )
    mqtt_client.loop_start()

    # Write a state to MQTT from another thread
    with ThreadPoolExecutor() as executor:
        future = executor.submit(discoverable._state_helper, "test")
        # Wait for executor to finish
        future.result(1)
        # Check that flag is set
        assert discoverable.wrote_configuration is True
        assert discoverable.config_message is not None

    # Wait until we receive the published message
    assert received_message.wait(1)


def test_publish_async(discoverable: Discoverable):
    received_message = Event()
    mqtt_client = Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5, userdata=received_message)

    mqtt_client.connect(host="localhost", clean_start=True)
    mqtt_client.on_message = message_callback
    mqtt_client.subscribe(
        (
            "hmd/binary_sensor/test/state/#",
            SubscribeOptions(retainHandling=SubscribeOptions.RETAIN_DO_NOT_SEND),
        )
    )
    mqtt_client.loop_start()

    # Write a state to MQTT from an asyncio event loop
    async def publish_state():
        discoverable._state_helper("test")

    asyncio.run(publish_state())

    # Wait until we receive the published message
    assert received_message.wait(1)


def test_disconnect_client(mocker: MockerFixture):
    """Test that the __del__ method disconnects from the broker"""
    mocked_client = mocker.patch("paho.mqtt.client.Client")
    mock_instance = mocked_client.return_value
    mock_instance.connect.return_value = MQTT_ERR_SUCCESS
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    discoverable = Discoverable[EntityInfo](settings)
    del discoverable

    mock_instance.disconnect.assert_called_once()
    mock_instance.loop_stop.assert_called_once()


def test_set_availability_topic(discoverable_availability: Discoverable):
    assert discoverable_availability.availability_topic is not None
    assert discoverable_availability.availability_topic == "hmd/binary_sensor/test/availability"


def test_config_availability_topic(discoverable_availability: Discoverable):
    config = discoverable_availability.generate_config()
    assert config.get("availability_topic") is not None


def test_set_availability(discoverable_availability: Discoverable):
    # Send availability message
    discoverable_availability.set_availability(True)

    # Receive a single message, ignoring retained messages
    availability_message = subscribe.simple(discoverable_availability.availability_topic, msg_count=1, retained=False)
    assert isinstance(availability_message, MQTTMessage)
    assert availability_message.payload.decode("utf-8") == "online"

    discoverable_availability.set_availability(False)


def test_set_availability_wrong_config(discoverable: Discoverable):
    """A discoverable that has not set availability to manual cannot invoke the \
        methods"""
    with pytest.raises(RuntimeError):
        discoverable.set_availability(True)


def test_set_attributes(discoverable: Discoverable):
    attributes = {"test attribute": "test"}
    discoverable.set_attributes(attributes)
