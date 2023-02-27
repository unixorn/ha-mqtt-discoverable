import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Button, ButtonInfo


@pytest.fixture(name="button")
def button() -> Button:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = ButtonInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define an empty `command_callback`
    return Button(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = ButtonInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define empty callback
    sensor = Button(settings, lambda *_: None)
    assert sensor is not None
