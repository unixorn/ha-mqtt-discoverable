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


def test_open(valve: Valve, position_valve: Valve):
    """Test to set a valve to open"""
    valve.open()
    position_valve.open()


def test_closed(valve: Valve, position_valve: Valve):
    """Test to set a valve to closed"""
    valve.closed()
    position_valve.closed()


def test_closing(valve: Valve, position_valve: Valve):
    """Test to set a valve to closing"""
    valve.closing()
    position_valve.closing()


def test_opening(valve: Valve, position_valve: Valve):
    """Test to set a valve to opening"""
    valve.opening()
    position_valve.opening()


def test_position(position_valve: Valve):
    """Test to set a position to the valve"""
    position_valve.position(42)


def test_position_and_state(position_valve: Valve):
    """Test to set a position and state to the valve"""
    position_valve.position(state="opening", position=42)


def test_reports_position_true_disables_payload_and_state_fields():
    """When reports_position=True, payload_* and state_* must be None (HA restriction)."""
    valve_info = ValveInfo(
        name="test",
        reports_position=True,
        payload_open="OPEN",
        payload_close="CLOSE",
        state_open="open",
        state_closed="closed",
    )

    assert valve_info.payload_open is None
    assert valve_info.payload_close is None
    assert valve_info.state_open is None
    assert valve_info.state_closed is None


@pytest.mark.parametrize("position", [-1, 101])
def test_set_position_out_of_range(position_valve: Valve, position: int):
    with pytest.raises(RuntimeError, match="out of range"):
        position_valve.position(position)


def test_set_position_as_non_int(position_valve: Valve):
    with pytest.raises(ValueError, match="Position should be an int not"):
        position_valve.position("50")


def test_set_position_not_supported(valve: Valve):
    with pytest.raises(RuntimeError, match="does not support position reporting"):
        valve.position(50)
