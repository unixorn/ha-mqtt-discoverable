#!/usr/bin/env python3
#
# sensors.py
#
# Copyright 2022, Joe Block <jpb@unixorn.net>

"""
Code to support the hmd-create-binary-sensor script
"""

import logging
import sys

from ha_mqtt_discoverable import __version__ as TOOL_VERSION
from ha_mqtt_discoverable.cli import create_base_parser
from ha_mqtt_discoverable.sensors import BinarySensor
from ha_mqtt_discoverable.settings import binary_sensor_settings


def binary_sensor_parser():
    parser = create_base_parser(
        description="Create a binary sensor on MQTT that will be autodiscovered by Home Assistant"
    )
    parser.add_argument(
        "--state",
        type=str.upper,
        choices=["OFF", "ON"],
        help="Set the binary sensor's state",
    )
    parser.add_argument(
        "--metric-name", type=str, required=True, help="What metric to create"
    )
    return parser


def binary_sensor_cli():
    parser = binary_sensor_parser()
    cli = parser.parse_args()
    loglevel = getattr(logging, cli.log_level.upper(), None)
    logFormat = "[%(asctime)s][%(levelname)8s][%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=loglevel, format=logFormat)
    logging.info("Set log level to %s", cli.log_level.upper())
    return cli


def create_binary_sensor():
    """
    Create a binary sensor from the command line, and set its state.
    """
    cli = binary_sensor_cli()
    if cli.version:
        print(f"ha-mqtt-discoverable version {TOOL_VERSION}")
        sys.exit(0)
    logging.info(f"cli: {cli}")
    settings = binary_sensor_settings(path=cli.settings_file, cli=cli)
    logging.info(f"{settings}")
    sensor = BinarySensor(settings=settings)
    if cli.state == "ON":
        sensor.on()
    else:
        sensor.off()
