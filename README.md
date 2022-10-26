# hass-mqtt-devices

A python 3 module that takes advantage of Home Assistant's MQTT discovery
protocol to create sensors without having to define anything on the HA side.

## Supported Types

### Binary Sensors

#### Usage

```py
from hass_mqtt_devices.sensors import BinarySensor

# Create a settings dictionary
#
# Mandatory Keys:
#  mqtt_server
#  mqtt_prefix - defaults to homeassistant
#  mqtt_user
#  mqtt_password
#  device_id
#  device_name
#  device_class
#
# Optional Keys:
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

## Scripts Provided

hass_mqtt_devices creates the following helper scripts you can use in your own shell scripts.

- `ham-create-binary-sensor` - Lets you create a binary sensor and set its state