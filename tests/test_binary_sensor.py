import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo


@pytest.fixture(name="sensor", params=["on", "custom_on"])
def binary_sensor(request) -> BinarySensor:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = BinarySensorInfo(name="test", payload_on=request.param)
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    return BinarySensor(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = BinarySensorInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, sensor=sensor_info)
    sensor = BinarySensor(settings)
    assert sensor is not None


def test_generate_config(sensor: BinarySensor):
    config = sensor.generate_config()

    assert config is not None
    # If we have defined a custom payload, check that is part of the output config
    if sensor._sensor.payload_on:
        assert config["payload_on"] == sensor._sensor.payload_on


def test_update_state(sensor: BinarySensor):
    sensor.on()
    sensor.off()
