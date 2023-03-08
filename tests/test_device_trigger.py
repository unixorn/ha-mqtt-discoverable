import pytest
from ha_mqtt_discoverable import DeviceInfo, Settings
from ha_mqtt_discoverable.sensors import DeviceTrigger, DeviceTriggerInfo


@pytest.fixture(name="device_trigger")
def device_trigger() -> DeviceTrigger:
    mqtt_settings = Settings.MQTT(host="localhost")
    device_info = DeviceInfo(name="test", identifiers="id")
    sensor_info = DeviceTriggerInfo(
        name="test",
        device=device_info,
        type="button_press",
        subtype="button_1",
        unique_id="test",
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return DeviceTrigger(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    device_info = DeviceInfo(name="test", identifiers="id")
    sensor_info = DeviceTriggerInfo(
        name="test",
        device=device_info,
        type="button_press",
        subtype="button_1",
        unique_id="test",
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    trigger = DeviceTrigger(settings)
    trigger.write_config()
    assert trigger is not None


def test_config_topic(device_trigger: DeviceTrigger):
    config = device_trigger.generate_config()
    assert config["topic"] == device_trigger.state_topic


def test_trigger(device_trigger: DeviceTrigger):
    device_trigger.trigger("my_payload")
