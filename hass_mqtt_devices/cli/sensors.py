#!/usr/bin/env python3
#
# device.py
#
# Copyright 2022, Joe Block <jpb@unixorn.net>

"""
Code to support the ham-create-binary-sensor script
"""

import argparse
import logging

from hass_mqtt_devices.settings import binary_sensor_settings
from hass_mqtt_devices.sensors import BinarySensor


def create_base_parser():
    """
    Parse the command line options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug setting", action="store_true")
    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        help="set log level",
        choices=["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"],
        default="INFO",
    )
    parser.add_argument(
        "--client-name", type=str, help="MQTT client name", default="cephalopod"
    )
    parser.add_argument(
        "--device-class",
        type=str,
        help="Home Assistant device class",
        default="binary_sensor",
    )
    parser.add_argument("--device-id", type=str, help="Device ID")
    parser.add_argument("--device-name", type=str, help="Device Name")
    parser.add_argument(
        "--mqtt-prefix", type=str, default="homeassistant", help="MQTT prefix"
    )
    parser.add_argument("--mqtt-user", type=str, help="MQTT user.")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password.")
    parser.add_argument("--mqtt-server", type=str, help="MQTT server.")
    parser.add_argument("--settings-file", type=str, help="Settings file.")
    return parser


def binary_sensor_parser():
    parser = create_base_parser()
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
    logging.info(f"cli: {cli}")
    settings = binary_sensor_settings(path=cli.settings_file, cli=cli)
    logging.info(f"{settings}")
    sensor = BinarySensor(settings=settings)
    if cli.state == "ON":
        sensor.on()
    else:
        sensor.off()
