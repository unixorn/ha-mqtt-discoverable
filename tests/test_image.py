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
from pydantic import ValidationError

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Image, ImageInfo


@pytest.fixture
def image(request) -> Image:
    url_topic, image_topic, image_encoding, content_type = request.param
    mqtt_settings = Settings.MQTT(host="localhost")
    image_info = ImageInfo(
        name="test_image", url_topic=url_topic, image_topic=image_topic, image_encoding=image_encoding, content_type=content_type
    )
    settings = Settings(mqtt=mqtt_settings, entity=image_info)
    return Image(settings)


def test_required_config():
    """Test to make sure an image instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    image_info = ImageInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=image_info)
    image = Image(settings)
    assert image is not None


def test_url_topic_and_image_topic_set_raises_exception():
    with pytest.raises(ValueError):
        ImageInfo(name="test", url_topic="url_to_publish_to", image_topic="image_to_publish_to")


def test_url_topic_encoding_set_raises_exception():
    with pytest.raises(ValueError):
        ImageInfo(name="test", url_topic="url_to_publish_to", image_encoding="b64")


def test_url_topic_content_type_set_raises_exception():
    with pytest.raises(ValueError):
        ImageInfo(name="test", url_topic="url_to_publish_to", content_type="image/jpeg")


def test_image_topic_invalid_encoding_set_raises_exception():
    with pytest.raises(ValidationError):
        ImageInfo(name="test", image_encoding="invalid_encoding", image_topic="image_to_publish_to")


def test_image_topic_no_content_type_set_raises_exception():
    with pytest.raises(ValueError):
        ImageInfo(name="test", image_topic="image_to_publish_to")


@pytest.mark.parametrize("image", [("topic_to_publish_to", None, None, None)], indirect=True)
def test_generate_config_url(image: Image):
    config = image.generate_config()
    # If url_topic is defined, check that is part of config
    if image._entity.url_topic:
        assert config["url_topic"] == image._entity.url_topic


@pytest.mark.parametrize("image", [(None, "image_to_publish_to", "b64", "image/png")], indirect=True)
def test_generate_config_image(image: Image):
    config = image.generate_config()
    # Ensure attributes for image publication are part of config
    if image._entity.image_topic:
        assert config["image_topic"] == image._entity.image_topic
    if image._entity.image_encoding:
        assert config["image_encoding"] == image._entity.image_encoding
    if image._entity.content_type:
        assert config["content_type"] == image._entity.content_type


@pytest.mark.parametrize("image", [("topic_to_publish_url_to", None, None, None)], indirect=True)
def test_set_url(image: Image):
    image_url = "http://camera.local/latest.jpg"

    with patch.object(image.mqtt_client, "publish") as mock_publish:
        image.set_url(image_url)
        mock_publish.assert_called_with(image._entity.url_topic, image_url, retain=True)


@pytest.mark.parametrize("image", [(None, "image_to_publish_to", "b64", "image/png")], indirect=True)
def test_set_blob(image: Image):
    image_blob = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV+/qGhFw"
        "Q4iDhmqkwVRUUepYhEslLZCqw4ml35Bk4YkxcVRcC04+LFYdXBx1tXBVRAEP0DcBSdFFynxf0mhRYwHx/14d+9x9w7wNipMMfzjg"
        "KKaeioeE7K5VSH4igD86MEM+kVmaIn0Ygau4+seHr7eRXmW+7k/R6+cNxjgEYjnmKabxBvE05umxnmfOMxKokx8Tjym0wWJH7kuO"
        "fzGuWizl2eG9UxqnjhMLBQ7WOpgVtIV4iniiKyolO/NOixz3uKsVGqsdU/+wlBeXUlzneYw4lhCAkkIkFBDGRWYiNKqkmIgRfsxF"
        "/+Q7U+SSyJXGYwcC6hCgWj7wf/gd7dGYXLCSQrFgMCLZX2MAMFdoFm3rO9jy2qeAL5n4Ept+6sNYPaT9HpbixwBfdvAxXVbk/aAy"
        "x1g8EkTddGWfDS9hQLwfkbflAMGboHuNae31j5OH4AMdbV8AxwcAqNFyl53eXdXZ2//nmn19wN6HHKqAAggmgAAAAlwSFlzAAAuI"
        "wAALiMBeKU/dgAAAAd0SU1FB+kFBAs3LBSX2/sAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAADElEQVQI1"
        "2NgYGAAAAAEAAEnNCcKAAAAAElFTkSuQmCC"
    )

    with patch.object(image.mqtt_client, "publish") as mock_publish:
        image.set_payload(image_blob)
        mock_publish.assert_called_with(image._entity.image_topic, image_blob, retain=True)


@pytest.mark.parametrize("image", [(None, "image_to_publish_to", "b64", "image/png")], indirect=True)
def test_set_empty_url_raises(image: Image):
    with pytest.raises(RuntimeError, match="Image URL cannot be empty"):
        image.set_url("")


@pytest.mark.parametrize("image", [(None, "image_to_publish_to", "b64", "image/png")], indirect=True)
def test_set_empty_payload_raises(image: Image):
    with pytest.raises(RuntimeError, match="Image payload cannot be empty"):
        image.set_payload("")
