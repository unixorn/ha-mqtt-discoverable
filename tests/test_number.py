import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Number, NumberInfo


@pytest.fixture()
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
