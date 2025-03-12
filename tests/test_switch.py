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
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo


@pytest.fixture
def switch() -> Switch:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define an empty `command_callback`
    return Switch(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define empty callback
    sensor = Switch(settings, lambda *_: None)
    assert sensor is not None


def test_change_state(switch: Switch):
    switch.on()
    switch.off()
