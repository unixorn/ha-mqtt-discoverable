
import pytest
from ha_mqtt_discoverable import DeviceInfo, Discoverable, Settings, EntityInfo


@pytest.fixture
def discoverable() -> Discoverable[EntityInfo]:
    mqtt_settings = Settings.MQTT(host="localhost", username="admin", password="password")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    return Discoverable[EntityInfo](settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    d = Discoverable(settings)
    assert d is not None


def test_missing_config():
    sensor_info = EntityInfo(name="test", component="binary_sensor")
    # Missing MQTT settings
    with pytest.raises(ValueError):
        settings = Settings(sensor=sensor_info) # type: ignore


def test_generate_config(discoverable: Discoverable):
    device_config = discoverable.generate_config()

    assert device_config is not None
    assert device_config['name'] == "test"
    assert device_config['component'] == "binary_sensor"
    assert device_config['state_topic'] == "homeassistant/binary_sensor/test/state"


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
    discoverable._sensor.device = device_info
    discoverable._sensor.unique_id = "test_sensor"
    config = discoverable.generate_config()
    
    # Check that the device info is put in the output config
    assert config['device'] is not None
    assert config['device']['name'] == "Test device"

    discoverable.write_config()


def test_device_missing_unique_id():
    device_info = DeviceInfo(name="Test device", identifiers="test_device_id")
    with pytest.raises(ValueError):    
        EntityInfo(name="test", component="binary_sensor", device=device_info)


def test_device_with_unique_id():
    device_info = DeviceInfo(name="Test device", identifiers="test_device_id")
    EntityInfo(name="test", component="binary_sensor", unique_id="id", device=device_info)


def test_name_with_space():
    mqtt_settings = Settings.MQTT(host="localhost", username="admin", password="password")
    sensor_info = EntityInfo(name="Name with space", component="binary_sensor")
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    d = Discoverable[EntityInfo](settings)
    d.write_config()


def test_custom_object_id():
    mqtt_settings = Settings.MQTT(host="localhost", username="admin", password="password")
    sensor_info = EntityInfo(name="Test name", component="binary_sensor", object_id="custom object id")
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    d = Discoverable[EntityInfo](settings)
    d.write_config()