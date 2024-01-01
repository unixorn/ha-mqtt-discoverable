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

import re

import yaml
from ha_mqtt_discoverable import CONFIGURATION_KEY_NAMES


def clean_string(raw: str) -> str:
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
