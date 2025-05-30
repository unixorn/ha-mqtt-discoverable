#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        https://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
from unittest.mock import patch

import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Select, SelectInfo


@pytest.fixture
def select() -> Select:
    mqtt_settings = Settings.MQTT(host="localhost")
    select_info = SelectInfo(name="test", options=["one", "two", "three"])
    settings = Settings(mqtt=mqtt_settings, entity=select_info)
    return Select(settings, lambda _, __, ___: None)


def test_required_config(select: Select):
    """Test to make sure a select instance can be created"""
    assert select is not None


def test_generate_config(select: Select):
    config = select.generate_config()
    assert config is not None


def test_select_invalid_option(select: Select):
    with pytest.raises(RuntimeError):
        select.select_option("four")


def test_select_valid_option(select: Select):
    with patch.object(select.mqtt_client, "publish") as mock_publish:
        select.select_option("two")
        mock_publish.assert_called_with(select.state_topic, "two", retain=True)


def test_raise_if_empty_str_is_selected(select: Select):
    with pytest.raises(RuntimeError):
        select.select_option("")
