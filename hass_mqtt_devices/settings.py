#!/usr/bin/env python3

import logging
from hass_mqtt_devices.utils import read_yaml_file


def load_mqtt_settings(path: str = None, cli=None) -> dict:
    """
    Base settings loader & validator

    Valid characters for object_id and node_id are [a-zA-Z0-9_-]
    """
    try:
        settings = read_yaml_file(path=path)
    except TypeError:
        settings = {}

    # CLI args override stuff in the settings file
    # if cli.data:
    #     settings["data"] = cli.data
    if cli.client_name:
        settings["client_name"] = cli.client_name
    if cli.device_class:
        settings["device_class"] = cli.device_class
    if cli.device_id:
        settings["device_id"] = cli.device_id
    if cli.device_name:
        settings["device_name"] = cli.device_name
    if cli.mqtt_password:
        settings["mqtt_password"] = cli.mqtt_password
    if cli.mqtt_prefix:
        settings["mqtt_prefix"] = cli.mqtt_prefix
    if cli.mqtt_server:
        settings["mqtt_server"] = cli.mqtt_server
    if cli.mqtt_user:
        settings["mqtt_user"] = cli.mqtt_user

    # Validate that we have all the settings data we need
    assert "device_class" in settings, "device_class is unset."
    assert "device_id" in settings, "device_id is unset."
    assert "device_name" in settings, "device_name is unset."
    assert "client_name" in settings, "client_name is unset."

    # if "data" not in settings:
    #     raise RuntimeError("No data was specified")
    if "device_name" not in settings:
        raise RuntimeError("No device_name was specified")
    if "mqtt_prefix" not in settings:
        raise RuntimeError("You need to specify an mqtt prefix")
    if "mqtt_user" not in settings:
        raise RuntimeError("No mqtt_user was specified")
    if "mqtt_password" not in settings:
        raise RuntimeError("No mqtt_password was specified")

    return settings


def sensor_delete_settings(path: str = None, cli=None) -> dict:
    """
    Load settings
    Valid characters for object_id and node_id are [a-zA-Z0-9_-]
    """
    try:
        settings = read_yaml_file(path=path)
    except TypeError:
        settings = {}

    # CLI args override stuff in the settings file
    if cli.client_name:
        settings["client_name"] = cli.client_name
    if cli.device_id:
        settings["device_id"] = cli.device_id
    if cli.device_name:
        settings["device_name"] = cli.device_name
    if cli.mqtt_password:
        settings["mqtt_password"] = cli.mqtt_password
    if cli.mqtt_prefix:
        settings["mqtt_prefix"] = cli.mqtt_prefix
    if cli.mqtt_server:
        settings["mqtt_server"] = cli.mqtt_server
    if cli.mqtt_user:
        settings["mqtt_user"] = cli.mqtt_user

    # Validate that we have all the settings data we need
    assert "device_id" in settings, "device_id is unset."
    assert "device_name" in settings, "device_name is unset."
    assert "client_name" in settings, "client_name is unset."

    # if "data" not in settings:
    #     raise RuntimeError("No data was specified")
    if "device_name" not in settings:
        raise RuntimeError("No device_name was specified")
    if "mqtt_prefix" not in settings:
        raise RuntimeError("You need to specify an mqtt prefix")
    if "mqtt_user" not in settings:
        raise RuntimeError("No mqtt_user was specified")
    if "mqtt_password" not in settings:
        raise RuntimeError("No mqtt_password was specified")


def binary_sensor_settings(path: str = None, cli=None) -> dict:
    """
    Load settings for a binary sensor
    """
    settings = load_mqtt_settings(path=path, cli=cli)
    settings["state"] = cli.state
    settings["metric_name"] = cli.metric_name
    logging.debug(f"settings: {settings}")
    return settings
