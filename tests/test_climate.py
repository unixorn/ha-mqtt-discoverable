import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Climate, ClimateInfo

# Test data
modes = ["off", "heat", "cool"]

@pytest.fixture
def climate() -> Climate:
    """Test climate temperature settings"""
    mqtt_settings = Settings.MQTT(host="localhost")
    climate_info = ClimateInfo(
        name="test_climate",
        temperature_unit="C",
        min_temp=16,
        max_temp=32,
        modes=modes
    )
    settings = Settings(mqtt=mqtt_settings, entity=climate_info)
    return Climate(settings, lambda *_: None)


def test_set_temperature(climate: Climate):
    """Test setting the temperature"""
    climate.set_temperature(20.0)

    # Test with out-of-range temperature
    with pytest.raises(RuntimeError):
        climate.set_temperature(15.0)  # Below min_temp
    with pytest.raises(RuntimeError):
        climate.set_temperature(33.0)  # Above max_temp

def test_climate_mode(climate: Climate):
    """Test climate mode settings"""
    # Valid mode
    climate.set_mode("heat")

    # Invalid mode
    with pytest.raises(RuntimeError):
        climate.set_mode("invalid_mode")
