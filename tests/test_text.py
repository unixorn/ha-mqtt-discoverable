import random
import string
import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Text, TextInfo


@pytest.fixture()
def text() -> Text:
    mqtt_settings = Settings.MQTT(host="localhost")
    text_info = TextInfo(name="test", min=5)
    settings = Settings(mqtt=mqtt_settings, entity=text_info)
    # Define empty callback
    return Text(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    text_info = TextInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=text_info)
    # Define empty callback
    text = Text(settings, lambda *_: None)
    assert text is not None


def test_set_text(text: Text):
    text.set_text("this is as test")


def test_too_short_string(text: Text):
    with pytest.raises(RuntimeError):
        text.set_text("t")


def test_too_long_string(text: Text):
    length = 500
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(length))
    with pytest.raises(RuntimeError):
        text.set_text(random_string)
