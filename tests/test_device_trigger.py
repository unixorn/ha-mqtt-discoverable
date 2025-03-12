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

from ha_mqtt_discoverable import DeviceInfo, Settings
from ha_mqtt_discoverable.sensors import DeviceTrigger, DeviceTriggerInfo


@pytest.fixture(name="device_trigger")
def device_trigger() -> DeviceTrigger:
    mqtt_settings = Settings.MQTT(host="localhost")
    device_info = DeviceInfo(name="test", identifiers="id")
    sensor_info = DeviceTriggerInfo(
        name="test",
        device=device_info,
        type="button_press",
        subtype="button_1",
        unique_id="test",
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return DeviceTrigger(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    device_info = DeviceInfo(name="test", identifiers="id")
    sensor_info = DeviceTriggerInfo(
        name="test",
        device=device_info,
        type="button_press",
        subtype="button_1",
        unique_id="test",
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    trigger = DeviceTrigger(settings)
    assert trigger is not None


def test_config_topic(device_trigger: DeviceTrigger):
    config = device_trigger.generate_config()
    assert config["topic"] == device_trigger.state_topic


def test_trigger(device_trigger: DeviceTrigger):
    device_trigger.trigger("my_payload")
