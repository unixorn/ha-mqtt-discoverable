import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Event
from paho.mqtt.client import (
    Client,
    MQTTMessage,
    MQTTv5,
    SubscribeOptions,
    MQTT_ERR_SUCCESS,
)
import pytest
from pytest_mock import MockerFixture
from ha_mqtt_discoverable import DeviceInfo, Discoverable, Settings, EntityInfo


@pytest.fixture
def discoverable() -> Discoverable[EntityInfo]:
    mqtt_settings = Settings.MQTT(
        host="localhost", username="admin", password="password"
    )
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
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


def test_discovery_topics():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    assert d._discovery_topic_prefix == "homeassistant/binary_sensor/test"
    assert d.config_topic == "homeassistant/binary_sensor/test/config"


def test_discovery_topics_with_device():
    mqtt_settings = Settings.MQTT(host="localhost")
    device = DeviceInfo(name="test_device", identifiers="id")
    sensor_info = EntityInfo(
        name="test", component="binary_sensor", device=device, unique_id="unique_id"
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    assert d._discovery_topic_prefix == "homeassistant/binary_sensor/test_device/test"
    assert d.config_topic == "homeassistant/binary_sensor/test_device/test/config"


def test_generate_config(discoverable: Discoverable):
    device_config = discoverable.generate_config()

    assert device_config is not None
    assert device_config["name"] == "test"
    assert device_config["component"] == "binary_sensor"
    assert device_config["state_topic"] == "homeassistant/binary_sensor/test/state"


def test_connect(discoverable: Discoverable):
    # Try to connect to MQTT
    discoverable._connect()
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
    EntityInfo(
        name="test", component="binary_sensor", unique_id="id", device=device_info
    )


def test_name_with_space():
    mqtt_settings = Settings.MQTT(
        host="localhost", username="admin", password="password"
    )
    sensor_info = EntityInfo(name="Name with space", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    d = Discoverable[EntityInfo](settings)
    d.write_config()


def test_custom_object_id():
    mqtt_settings = Settings.MQTT(
        host="localhost", username="admin", password="password"
    )
    sensor_info = EntityInfo(
        name="Test name", component="binary_sensor", object_id="custom object id"
    )
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
    # If the broker is `dirty` and contains messages send by other test functions, skip these retained messages
    if message.retain:
        logging.warn("Skipping retained message")
        return
    payload = message.payload.decode()
    assert "test" in payload
    userdata.set()
    client.disconnect()


def test_publish_multithread(discoverable: Discoverable):
    received_message = Event()
    mqtt_client = Client(protocol=MQTTv5, userdata=received_message)

    mqtt_client.connect(host="localhost")
    mqtt_client.on_message = message_callback
    mqtt_client.subscribe(
        (
            "homeassistant/binary_sensor/test/state/#",
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
    mqtt_client = Client(protocol=MQTTv5, userdata=received_message)

    mqtt_client.connect(host="localhost", clean_start=True)
    mqtt_client.on_message = message_callback
    mqtt_client.subscribe(
        (
            "homeassistant/binary_sensor/test/state/#",
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
    mqtt_settings = Settings.MQTT(
        host="localhost", username="admin", password="password"
    )
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    discoverable = Discoverable[EntityInfo](settings)
    del discoverable

    mock_instance.disconnect.assert_called_once()
    mock_instance.loop_stop.assert_called_once()
