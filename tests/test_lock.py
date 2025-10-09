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
from unittest.mock import patch

import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Lock, LockInfo


@pytest.fixture
def lock() -> Lock:
    mqtt_settings = Settings.MQTT(host="localhost")
    lock_info = LockInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=lock_info)
    return Lock(settings, lambda _, __, ___: None)


def test_required_config(lock: Lock):
    """Test to make sure a lock instance can be created"""
    assert lock is not None


def test_generate_config(lock: Lock):
    config = lock.generate_config()
    assert config is not None


def test_lock_state_locked(lock: Lock):
    with patch.object(lock.mqtt_client, "publish") as mock_publish:
        lock.locked()
        mock_publish.assert_called_with(lock.state_topic, lock._entity.state_locked, retain=True)


def test_lock_state_locking(lock: Lock):
    with patch.object(lock.mqtt_client, "publish") as mock_publish:
        lock.locking()
        mock_publish.assert_called_with(lock.state_topic, lock._entity.state_locking, retain=True)


def test_lock_state_unlocked(lock: Lock):
    with patch.object(lock.mqtt_client, "publish") as mock_publish:
        lock.unlocked()
        mock_publish.assert_called_with(lock.state_topic, lock._entity.state_unlocked, retain=True)


def test_lock_state_unlocking(lock: Lock):
    with patch.object(lock.mqtt_client, "publish") as mock_publish:
        lock.unlocking()
        mock_publish.assert_called_with(lock.state_topic, lock._entity.state_unlocking, retain=True)


def test_lock_state_jammed(lock: Lock):
    with patch.object(lock.mqtt_client, "publish") as mock_publish:
        lock.jammed()
        mock_publish.assert_called_with(lock.state_topic, lock._entity.state_jammed, retain=True)
