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
import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Light, LightInfo

# Test data
color_modes = ["rgb", "rgbw"]
effects = ["rainbow", "mycustomeffect"]


@pytest.fixture
def light() -> Light:
    """Return a light instance"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = LightInfo(
        name="test",
        color_mode=True,
        supported_color_modes=color_modes,
        effect=True,
        effect_list=effects,
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Light(settings, lambda *_: None)


def test_required_config():
    """Test to make sure a light instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = LightInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Light(settings, lambda *_: None)
    assert sensor is not None


def test_on_off(light: Light):
    """Test to toggle a light"""
    light.on()
    light.off()


@pytest.mark.parametrize("brightness", [0, 255])
def test_brightness(light: Light, brightness: int):
    """Test to set the brightness"""
    light.brightness(brightness)


@pytest.mark.parametrize("brightness", [-1, 256])
def test_brightness_out_of_range(light: Light, brightness):
    """Test to make sure brightness can't be set out of bounds"""
    with pytest.raises(RuntimeError):
        light.brightness(brightness)


@pytest.mark.parametrize("color_modes", color_modes)
def test_color(light: Light, color_modes):
    """Test to set the color"""
    light.color(color_modes, {"test": 123})


def test_color_unsupported(light: Light):
    """Test to make sure we can't use a color mode that is unsupported"""
    with pytest.raises(RuntimeError):
        light.color("test", {"r": 255, "g": 255, "b": 255})


@pytest.mark.parametrize("effects", effects)
def test_effect(light: Light, effects):
    """Test to enable effect"""
    light.effect(effects)


def test_effect_unsupported(light: Light):
    """Test to make sure we can't use unsupported effects"""
    with pytest.raises(RuntimeError):
        light.effect("unsupported_effect")
