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
from ha_mqtt_discoverable.sensors import Valve, ValveInfo


@pytest.fixture
def valve() -> Valve:
    """Return a valve instance"""
    mqtt_settings = Settings.MQTT(host="localhost")
    valve_info = ValveInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=valve_info)
    return Valve(settings, lambda _, __, ___: None)


@pytest.fixture
def position_valve() -> Valve:
    """Return a valve instance that is position controlled"""
    mqtt_settings = Settings.MQTT(host="localhost")
    valve_info = ValveInfo(name="test", reports_position=True)
    settings = Settings(mqtt=mqtt_settings, entity=valve_info)
    return Valve(settings, lambda _, __, ___: None)


def test_required_config():
    """Test to make sure a valve instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    valve_info = ValveInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=valve_info)
    valve = Valve(settings, lambda _, __, ___: None)
    assert valve is not None


def test_open(valve: Valve):
    """Test to set a valve to open"""
    valve.open()


def test_closed(valve: Valve):
    """Test to set a valve to closed"""
    valve.closed()


def test_closing(valve: Valve):
    """Test to set a valve to closing"""
    valve.closing()


def test_opening(valve: Valve):
    """Test to set a valve to opening"""
    valve.opening()


def test_position(position_valve: Valve):
    """Test to set a position to the valve"""
    position_valve.position(42)


def test_position_and_state(position_valve: Valve):
    """Test to set a position and state to the valve"""
    position_valve.position(state="opening", position=42)


@pytest.mark.parametrize("position", [-1, 101])
def test_set_position_out_of_range(position_valve: Valve, position: int):
    with pytest.raises(RuntimeError, match="out of range"):
        position_valve.position(position)


def test_set_position_not_supported(valve: Valve):
    with pytest.raises(RuntimeError, match="does not support position reporting"):
        valve.position(50)
