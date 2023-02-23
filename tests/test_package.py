from ha_mqtt_discoverable import __version__


def test_read_version():
    assert __version__ is not None
