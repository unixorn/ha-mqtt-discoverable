import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo


@pytest.fixture(params=["°C", "kWh"])
def sensor(request) -> Sensor:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SensorInfo(name="test", unit_of_measurement=request.param)
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Sensor(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SensorInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Sensor(settings)
    assert sensor is not None


def test_generate_config(sensor: Sensor):
    config = sensor.generate_config()

    assert config is not None
    # If we have defined a custom unit of measurement, check that is part of the output config
    if sensor._entity.unit_of_measurement:
        assert config["unit_of_measurement"] == sensor._entity.unit_of_measurement


def test_update_state(sensor: Sensor):
    sensor.set_state(1)
