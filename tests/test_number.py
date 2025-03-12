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
from ha_mqtt_discoverable.sensors import Number, NumberInfo


@pytest.fixture
def number() -> Number:
    mqtt_settings = Settings.MQTT(host="localhost")
    number_info = NumberInfo(name="test", min=5.0, max=90.0)
    settings = Settings(mqtt=mqtt_settings, entity=number_info)
    # Define empty callback
    return Number(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    number_info = NumberInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=number_info)
    # Define empty callback
    number = Number(settings, lambda *_: None)
    assert number is not None


def test_set_value(number: Number):
    number.set_value(42.0)


def test_number_too_small(number: Number):
    with pytest.raises(RuntimeError):
        number.set_value(4.0)


def test_number_too_large(number: Number):
    with pytest.raises(RuntimeError):
        number.set_value(91.0)
