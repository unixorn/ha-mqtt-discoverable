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
COLOR_MODES: list[str] = ["rgb", "rgbw"]
EFFECTS: list[str] = ["rainbow", "my_custom_effect"]


@pytest.fixture
def make_light():
    def _make_light(color_mode: bool | None = None, effect: bool = False, supported_color_modes=None, effect_list=None):
        """Return a light instance"""
        mqtt_settings = Settings.MQTT(host="localhost")
        sensor_info = LightInfo(
            name="test",
            color_mode=color_mode,
            supported_color_modes=supported_color_modes,
            effect=effect,
            effect_list=effect_list,
        )
        settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
        return Light(settings, lambda _, __, ___: None)

    return _make_light


@pytest.fixture
def light_no_color_mode_and_effect_support(make_light) -> Light:
    return make_light()


@pytest.fixture
def light(make_light) -> Light:
    """Return a light instance"""
    return make_light(color_mode=True, effect=True, supported_color_modes=COLOR_MODES, effect_list=EFFECTS)


def test_required_config():
    """Test to make sure a light instance can be created"""
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = LightInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Light(settings, lambda _, __, ___: None)
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


@pytest.mark.parametrize("color_modes", COLOR_MODES)
def test_color(light: Light, color_modes):
    """Test to set the color"""
    light.color(color_modes, {"test": 123})


def test_color_mode_not_set(make_light):
    """Test to make sure we can't use a color mode if supported_color_modes is not set"""
    light = make_light(color_mode=True, supported_color_modes=None)
    with pytest.raises(RuntimeError, match="List of supported color modes cannot be empty"):
        light.color("rgb", {"r": 255, "g": 255, "b": 255})


def test_color_mode_unsupported(light: Light):
    """Test to make sure we can't use a color mode that is unsupported"""
    with pytest.raises(RuntimeError):
        light.color("test", {"r": 255, "g": 255, "b": 255})


@pytest.mark.parametrize("effects", EFFECTS)
def test_effect(light: Light, effects):
    """Test to enable effect"""
    light.effect(effects)


def test_effect_not_set(make_light):
    """Test to make sure we can't use an effect if effect_list is not set"""
    light = make_light(effect=True, effect_list=None)
    with pytest.raises(RuntimeError, match="List of supported effects cannot be empty"):
        light.effect("rainbow")


def test_effect_unsupported(light: Light):
    """Test to make sure we can't use unsupported effects"""
    with pytest.raises(RuntimeError, match="Effect is not within configured effect_list"):
        light.effect("unsupported_effect")


def test_effects_disabled(light_no_color_mode_and_effect_support: Light):
    """Test to make sure we can't set effects if disabled"""
    with pytest.raises(RuntimeError, match="does not support effects"):
        light_no_color_mode_and_effect_support.effect("rainbow")


def test_color_mode_disabled(light_no_color_mode_and_effect_support: Light):
    """Test to make sure we can't set color modes if disabled"""
    with pytest.raises(RuntimeError, match="does not support setting color"):
        light_no_color_mode_and_effect_support.color("rgb", {"test": 123})
