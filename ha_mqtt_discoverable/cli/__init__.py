#
# Common cli functions for hmd tooling
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
    parser.add_argument("--client-name", type=str, help="MQTT client name", default="cephalopod")
    parser.add_argument(
        "--device-class",
        type=str,
        help="Home Assistant device class",
        default="binary_sensor",
    )
    parser.add_argument("--device-id", type=str, help="Device ID")
    parser.add_argument("--device-name", type=str, help="Device Name")
    parser.add_argument("--icon", type=str, help="Icon")
    parser.add_argument("--mqtt-prefix", type=str, default="homeassistant", help="MQTT prefix")
    parser.add_argument("--mqtt-user", type=str, help="MQTT user.")
    parser.add_argument("--mqtt-password", type=str, help="MQTT password.")
    parser.add_argument("--mqtt-server", type=str, help="MQTT server.")
    parser.add_argument("--mqtt-port", type=str, help="MQTT port.", default=1883)
    parser.add_argument("--settings-file", type=str, help="Settings file.")

    parser.add_argument("--use-tls", "--use-ssl", action="store_true", help="Use TLS.")
    parser.add_argument("--tls-ca-cert", type=str, help="Path to CA cert.")
    parser.add_argument("--tls-certfile", type=str, help="Path to certfile.")
    parser.add_argument("--tls-key", type=str, help="Path to tls key.")

    parser.add_argument("--version", "-v", help="Show version and exit", action="store_true")
    return parser


def module_version():
    print(MODULE_VERSION)
