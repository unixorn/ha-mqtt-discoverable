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
from ha_mqtt_discoverable.sensors import Cover, CoverInfo


@pytest.fixture
def cover() -> Cover:
    """Return a cover instance"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = CoverInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Cover(settings, lambda *_: None)


def test_required_config():
    """Test to make sure a cover instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = CoverInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Cover(settings, lambda *_: None)
    assert sensor is not None


def test_open(cover: Cover):
    """Test to set a cover to open"""
    cover.open()


def test_closed(cover: Cover):
    """Test to set a cover to closed"""
    cover.closed()


def test_closing(cover: Cover):
    """Test to set a cover to closing"""
    cover.closing()


def test_opening(cover: Cover):
    """Test to set a cover to opening"""
    cover.opening()


def test_stopped(cover: Cover):
    """Test to set a cover to stopped"""
    cover.stopped()
