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
from ha_mqtt_discoverable.sensors import Camera, CameraInfo


@pytest.fixture
def camera() -> Camera:
    mqtt_settings = Settings.MQTT(host="localhost")
    camera_info = CameraInfo(name="test", topic="topic_to_publish_image_payload_to")
    settings = Settings(mqtt=mqtt_settings, entity=camera_info)
    return Camera(settings, lambda _, __, ___: None)


def test_required_config(camera: Camera):
    """Test to make sure a lock instance can be created"""
    assert camera is not None


def test_generate_config(camera: Camera):
    config = camera.generate_config()
    assert config is not None


def test_set_empty_image_payload_raises(camera: Camera):
    with pytest.raises(RuntimeError, match="Image payload of the camera cannot be empty"):
        camera.set_payload("")


def test_set_empty_image_payload_successful(camera: Camera):
    image_payload: bytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"
    with patch.object(camera.mqtt_client, "publish") as mock_publish:
        camera.set_payload(image_payload)
        mock_publish.assert_called_with(camera._entity.topic, image_payload, retain=True)
