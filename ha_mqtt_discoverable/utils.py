#!/usr/bin/env python3
#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import re

import yaml
from ha_mqtt_discoverable import CONFIGURATION_KEY_NAMES


def clean_string(raw: str = None) -> str:
    """
    MQTT Discovery protocol only allows [a-zA-Z0-9_-]
    """
    result = re.sub(r"[^A-Za-z0-9_-]", "-", raw)
    return result


def read_yaml_file(path: str = None) -> dict:
    """
    Return the data structure contained in a yaml file

    Args:
        path (str): Path to read from

    Returns:
        Data decoded from YAML file content
    """
    with open(path) as yamlFile:
        data = yaml.safe_load(yamlFile)
        return data


def valid_configuration_key(name: str) -> bool:
    """
    Confirm that a configuration key is in the allowed list
    """
    return name in CONFIGURATION_KEY_NAMES
