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
from unittest.mock import patch

import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Valve, ValveInfo


@pytest.fixture
def make_valve():
    def _make_valve(
        reports_position: bool = False,
        payload_open: str | None = "OPEN",
        payload_close: str | None = "CLOSE",
        state_open: str | None = "open",
        state_closed: str | None = "closed",
    ):
        """Return a valve instance"""
        mqtt_settings = Settings.MQTT(host="localhost")
        sensor_info = ValveInfo(
            name="test",
            reports_position=reports_position,
            payload_open=payload_open,
            payload_close=payload_close,
            state_open=state_open,
            state_closed=state_closed,
        )
        settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
        return Valve(settings, lambda _, __, ___: None)

    return _make_valve


@pytest.fixture
def valve(make_valve) -> Valve:
    """Return a valve instance"""
    return make_valve()


@pytest.fixture
def position_valve(make_valve) -> Valve:
    """Return a valve instance that is position controlled"""
    return make_valve(reports_position=True, payload_open=None, payload_close=None, state_open=None, state_closed=None)


def test_required_config():
    """Test to make sure a valve instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    valve_info = ValveInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=valve_info)
    valve = Valve(settings, lambda _, __, ___: None)
    assert valve is not None


def test_open(valve: Valve, position_valve: Valve):
    """Test to set a valve to open"""
    with patch.object(valve.mqtt_client, "publish") as mock_publish:
        valve.open()
        mock_publish.assert_called_with(valve.state_topic, valve._entity.state_open, retain=False)
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.open()
        mock_publish.assert_called_with(position_valve.state_topic, position_valve._entity.position_open, retain=False)


def test_closed(valve: Valve, position_valve: Valve):
    """Test to set a valve to closed"""
    with patch.object(valve.mqtt_client, "publish") as mock_publish:
        valve.closed()
        mock_publish.assert_called_with(valve.state_topic, valve._entity.state_closed, retain=False)
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.closed()
        mock_publish.assert_called_with(position_valve.state_topic, position_valve._entity.position_closed, retain=False)


def test_closing(valve: Valve, position_valve: Valve):
    """Test to set a valve to closing"""
    with patch.object(valve.mqtt_client, "publish") as mock_publish:
        valve.closing()
        mock_publish.assert_called_with(valve.state_topic, valve._entity.state_closing, retain=False)
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.closing()
        mock_publish.assert_called_with(position_valve.state_topic, position_valve._entity.state_closing, retain=False)


def test_opening(valve: Valve, position_valve: Valve):
    """Test to set a valve to opening"""
    with patch.object(valve.mqtt_client, "publish") as mock_publish:
        valve.opening()
        mock_publish.assert_called_with(valve.state_topic, valve._entity.state_opening, retain=False)
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.opening()
        mock_publish.assert_called_with(position_valve.state_topic, position_valve._entity.state_opening, retain=False)


def test_position(position_valve: Valve):
    """Test to set a position to the valve"""
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.position(42)
        mock_publish.assert_called_with(position_valve.state_topic, 42, retain=False)


def test_position_and_state(position_valve: Valve):
    """Test to set a position and state to the valve"""
    with patch.object(position_valve.mqtt_client, "publish") as mock_publish:
        position_valve.position(42, "opening")
        mock_publish.assert_called_with(position_valve.state_topic, '{"state": "opening", "position": 42}', retain=False)


def test_reports_position_true_disables_payload_and_state_fields():
    """When reports_position=True, payload_* and state_* must be None (HA restriction)."""
    with pytest.raises(
        ValueError, match="payload_open, payload_close, state_open and state_closed should not be set when using reports_position."
    ):
        ValveInfo(
            name="test",
            reports_position=True,
            payload_open="OPEN",
            payload_close="CLOSE",
            state_open="open",
            state_closed="closed",
        )


@pytest.mark.parametrize("position", [-1, 101])
def test_set_position_out_of_range(position_valve: Valve, position: int):
    with pytest.raises(RuntimeError, match="out of range"):
        position_valve.position(position)


def test_set_position_as_non_int(position_valve: Valve):
    with pytest.raises(ValueError, match="Position for valve should be an int not"):
        position_valve.position("50")  # type: ignore[arg-type]


def test_set_position_not_supported(valve: Valve):
    with pytest.raises(RuntimeError, match="does not support position reporting"):
        valve.position(50)
