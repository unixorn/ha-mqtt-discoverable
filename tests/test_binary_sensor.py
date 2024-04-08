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
import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo


@pytest.fixture(name="sensor", params=["on", "custom_on"])
def binary_sensor(request) -> BinarySensor:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = BinarySensorInfo(name="test", payload_on=request.param)
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return BinarySensor(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = BinarySensorInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = BinarySensor(settings)
    assert sensor is not None


def test_generate_config(sensor: BinarySensor):
    config = sensor.generate_config()

    assert config is not None
    # If we have defined a custom payload, check that is part of the output config
    if sensor._entity.payload_on:
        assert config["payload_on"] == sensor._entity.payload_on


def test_update_state(sensor: BinarySensor):
    sensor.on()
    sensor.off()


def test_boolean_state(sensor: BinarySensor):
    sensor.update_state(True)
    sensor.update_state(False)
