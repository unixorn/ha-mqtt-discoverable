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
from unittest.mock import patch

import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Image, ImageInfo


@pytest.fixture
def image() -> Image:
    mqtt_settings = Settings.MQTT(host="localhost")
    image_info = ImageInfo(name="test", url_topic="topic_to_publish_url_to")
    settings = Settings(mqtt=mqtt_settings, entity=image_info)
    return Image(settings)


def test_required_config():
    """Test to make sure an image instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    image_info = ImageInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=image_info)
    image = Image(settings)
    assert image is not None


def test_generate_config(image: Image):
    config = image.generate_config()

    assert config is not None
    # If we have defined an url_topic, check that is part of the output config
    if image._entity.url_topic:
        assert config["url_topic"] == image._entity.url_topic


def test_set_url(image: Image):
    image_url = "http://camera.local/latest.jpg"

    with patch.object(image.mqtt_client, "publish") as mock_publish:
        image.set_url(image_url)
        mock_publish.assert_called_with(image._entity.url_topic, image_url, retain=True)
