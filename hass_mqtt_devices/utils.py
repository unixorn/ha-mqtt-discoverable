#
# Copyright 2022 Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import yaml


def read_yaml_file(path: str = None):
    """
    Return the data structure contained in a yaml file

    Args:
        path (str): Path to read from

    Returns:
        Data decoded from YAML file content
    """
    with open(path) as yamlFile:
        data = yaml.load(yamlFile, Loader=yaml.FullLoader)
        return data
