"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pytest
from ha_mqtt_discoverable import EntityInfo, Settings


@pytest.fixture
def sensor_info_default():
    return EntityInfo(name="test", component="sensor")


def test_force_update_default(sensor_info_default):
    settings = Settings(mqtt=Settings.MQTT(host="localhost"), entity=sensor_info_default)
    config = settings.entity.model_dump(exclude_none=True, by_alias=True)
    assert config.get("force_update") is None


def test_force_update_true():
    info = EntityInfo(name="pulse", component="sensor", force_update=True)
    settings = Settings(mqtt=Settings.MQTT(host="localhost"), entity=info)
    config = settings.entity.model_dump(exclude_none=True, by_alias=True)
    assert config.get("force_update") is True
