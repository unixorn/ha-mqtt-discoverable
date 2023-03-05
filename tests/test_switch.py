import pytest
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo


@pytest.fixture()
def switch() -> Switch:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define an empty `command_callback`
    return Switch(settings, lambda *_: None)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SwitchInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    # Define empty callback
    sensor = Switch(settings, lambda *_: None)
    assert sensor is not None


def test_change_state(switch: Switch):
    switch.on()
    switch.off()
