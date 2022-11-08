#!/usr/bin/env python3
#
# Common cli functions for hmd tooling
#
# Copyright 2022, Joe Block <jpb@unixorn.net>

import argparse

from ha_mqtt_discoverable import __version__ as MODULE_VERSION


def create_base_parser(description: str = "Base parser"):
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
    parser.add_argument("--icon", type=str, help="Icon")
    parser.add_argument(
        "--mqtt-prefix", type=str, default="homeassistant", help="MQTT prefix"
    )
    parser.add_argument("--mqtt-user", type=str, help="MQTT user.")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password.")
    parser.add_argument("--mqtt-server", type=str, help="MQTT server.")
    parser.add_argument("--settings-file", type=str, help="Settings file.")

    parser.add_argument("--use-tls", "--use-ssl", action="store_true", help="Use TLS.")
    parser.add_argument("--tls-ca-cert", type=str, help="Path to CA cert.")
    parser.add_argument("--tls-certfile", type=str, help="Path to certfile.")
    parser.add_argument("--tls-key", type=str, help="Path to tls key.")

    parser.add_argument(
        "--version", "-v", help="Show version and exit", action="store_true"
    )
    return parser


def module_version():
    print(MODULE_VERSION)
