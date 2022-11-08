<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [ha-mqtt-discoverable](#ha-mqtt-discoverable)
  - [Installing](#installing)
    - [Python](#python)
    - [Docker](#docker)
  - [Supported Types](#supported-types)
    - [Binary Sensors](#binary-sensors)
      - [Usage](#usage)
    - [Devices](#devices)
      - [Usage](#usage-1)
  - [Scripts Provided](#scripts-provided)
    - [`hmd`](#hmd)
    - [`hmd create binary sensor`](#hmd-create-binary-sensor)
    - [`hmd create device`](#hmd-create-device)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# ha-mqtt-discoverable

A python 3 module that takes advantage of HA(Home Assistant('s MQTT discovery protocol to create sensors without having to define anything on the HA side.

Using MQTT discoverable devices lets us add new sensors and devices to HA without having to restart HA. This module includes scripts to make it easy to create discoverable devices from the command line if you don't want to bother writing python.

## Installing

### Python

`pip install ha-mqtt-discoverable` if you want to use it in your python scripts. This will also install the `hmd` utility scripts.

### Docker

If all you want to do is use the command line tools, the simplest way is to use them with `docker` or `nerdctl`. It won't interfere with your system python and potentially cause you issues there. You can use the [unixorn/ha-mqtt-discoverable](https://hub.docker.com/repository/docker/unixorn/ha-mqtt-discoverable) image on dockerhub directly, but if you add `$reporoot/bin` to your `$PATH`, the `hmd` script in there will automatically run the command line tools inside a docker container with `docker` or `nerdctl`, depending on what it finds in your `$PATH`.

## Supported Types

### Binary Sensors

#### Usage

Here is an example that creates a binary sensor.

```py
from ha_mqtt_discoverable.sensors import BinarySensor

# Create a settings dictionary
#
# Mandatory Keys:
#  mqtt_server
#  mqtt_user
#  mqtt_password
#  device_id
#  device_name
#  device_class
#
# Optional Keys:
#  mqtt_prefix - defaults to homeassistant
#  payload_off
#  payload_on
#  unique_id

configd = {
    "mqtt_server": "mqtt.example.com",
    "mqtt_prefix": "homeassistant",
    "mqtt_user": "mqtt_user",
    "mqtt_password": "mqtt_password",
    "device_id": "device_id",
    "device_name":"MySensor",
    "device_class":"motion",
}

mysensor = BinarySensor(settings=configd)
mysensor.on()
mysensor.off()

```

### Devices

#### Usage

Here's an example that will create a MQTT device and add multiple sensors to it.

```py
from ha_mqtt_discoverable.device import Device

# Create a settings dictionary
#
# Mandatory Keys:
#  mqtt_server
#  mqtt_user
#  mqtt_password
#  device_id
#  device_name
#  device_class
#  unique_id
#
# Optional Keys:
#  client_name
#  manufacturer
#  model
#  mqtt_prefix - defaults to homeassistant

configd = {
    "mqtt_server": "mqtt.example.com",
    "mqtt_prefix": "homeassistant",
    "mqtt_user": "mqtt_user",
    "mqtt_password": "mqtt_password",
    "device_id": "device_id",
    "device_name":"MySensor",
    "device_class":"motion",
    "manufacturer":"Acme Products",
    "model": "Rocket Skates",
}

device = Device(settings=configd)

# You can add more than one metric to a device
device.add_metric(
    name="Left skate thrust",
    value=33,
    configuration={"name": f"Left Skate Thrust"},
)
device.add_metric(
    name="Right skate thrust",
    value=33,
    configuration={"name": f"Right Skate Thrust"},
)

# Nothing gets written to MQTT until we publish
device.publish()

# Do your own code

# If we add a metric using the same name as an existing metric, the value is updated
device.add_metric(
    name="Right skate thrust",
    value=99,
    configuration={"name": f"Right Skate Thrust"},
)
device.publish()
```

## Scripts Provided

The `ha_mqtt_discoverable` module also installs the following helper scripts you can use in your own shell scripts.

### `hmd`

Uses the [gitlike-commands](https://github.com/unixorn/gitlike-commands/) module to find and execute `hmd` subcommands. Allows you to run `hmd create binary sensor` and `hmd` will find and run `hmd-create-binary-sensor` and pass it all the command line options.

### `hmd create binary sensor`

Create/Update a binary sensor and set its state.

Usage: `hmd create binary sensor --device-name mfsmaster --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --client-name inquisition --mqtt-server mqtt.unixorn.net --metric-name tamper --device-class motion --state off`

### `hmd create device`

Create/Update a device and set the state of multiple metrics on it.

Usage: `hmd create device --device-name coyote --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --mqtt-server mqtt.example.com --model 'Rocket Skates' --manufacturer 'Acme Products' --metric-data '{"name":"Left Rocket Skate","value":93}' --metric-data '{"name":"Right Rocket Skate","value":155}' --unique-id 'hmd-26536'`
