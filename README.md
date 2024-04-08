# ha-mqtt-discoverable

[![License](https://img.shields.io/github/license/unixorn/ha-mqtt-discoverable.svg)](https://opensource.org/license/apache-2-0/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unixorn/ha-mqtt-discoverable/main.svg)](https://github.com/unixorn/ha-mqtt-discoverable)
[![Downloads](https://static.pepy.tech/badge/ha-mqtt-discoverable)](https://pepy.tech/project/ha-mqtt-discoverable)

A Python 3 module that takes advantage of Home Assistant's [MQTT discovery protocol](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery) to create sensors without having to define anything on the HA side.

Using MQTT discoverable devices lets us add new sensors and devices to HA without having to restart HA. The `ha-mqtt-discoverable-cli` module includes scripts to make it easy to create discoverable devices from the command line if you don't want to bother writing Python.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Installing](#installing)
  - [Python](#python)
- [Supported entities](#supported-entities)
  - [Binary sensor](#binary-sensor)
    - [Usage](#usage)
  - [Button](#button)
  - [Device](#device)
    - [Usage](#usage-1)
  - [Device trigger](#device-trigger)
      - [Usage](#usage-2)
  - [Switch](#switch)
    - [Usage](#usage-3)
  - [Light](#light)
    - [Usage](#usage-4)
  - [Covers](#covers)
    - [Usage](#usage-5)
  - [Text](#text)
    - [Usage](#usage-6)
  - [Number](#number)
    - [Usage](#usage-7)
- [Contributing](#contributing)
- [Users of ha-mqtt-discoverable](#users-of-ha-mqtt-discoverable)
- [Contributors](#contributors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installing

### Python

ha-mqtt-discoverable runs on Python 3.10 or later.

`pip install ha-mqtt-discoverable` if you want to use it in your own python scripts. This will also install the `hmd` utility scripts.

<!-- Please keep the entities in alphabetical order -->
## Supported entities

The following Home Assistant entities are currently implemented:

- Binary sensor
- Button
- Cover
- Device
- Device trigger
- Light
- Number
- Sensor
- Switch
- Text

Each entity can associated to a device. See below for details.

### Binary sensor

#### Usage

The following example creates a binary sensor and sets its state:

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo


# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the sensor
sensor_info = BinarySensorInfo(name="MySensor", device_class="motion")

settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

# Instantiate the sensor
mysensor = BinarySensor(settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
mysensor.on()
mysensor.off()

# Or, change the state using a boolean
mysensor.update_state(True)
mysensor.update_state(False)

# You can also set custom attributes on the sensor via a Python dict
mysensor.set_attributes({"my attribute": "awesome"})

```

### Button

The button publishes no state, it simply receives a command from HA.

You must call `write_config` on a Button after creating it to make it discoverable.

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Button, ButtonInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the button
button_info = ButtonInfo(name="test")

settings = Settings(mqtt=mqtt_settings, entity=button_info)

# To receive button commands from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    perform_my_custom_action()

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the button
my_button = Button(settings, my_callback, user_data)

# Publish the button's discoverability message to let HA automatically notice it
my_button.write_config()

```

### Device
From the [Home Assistant documentation](https://developers.home-assistant.io/docs/device_registry_index):
> A device is a special entity in Home Assistant that is represented by one or more entities.
A device is automatically created when an entity defines its `device` property.
A device will be matched up with an existing device via supplied identifiers or connections, like serial numbers or MAC addresses.

#### Usage

The following example create a device, by associating multiple sensors to the same `DeviceInfo` instance.

```py
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Define the device. At least one of `identifiers` or `connections` must be supplied
device_info = DeviceInfo(name="My device", identifiers="device_id")

# Associate the sensor with the device via the `device` parameter
# `unique_id` must also be set, otherwise Home Assistant will not display the device in the UI
motion_sensor_info = BinarySensorInfo(name="My motion sensor", device_class="motion", unique_id="my_motion_sensor", device=device_info)

motion_settings = Settings(mqtt=mqtt_settings, entity=motion_sensor_info)

# Instantiate the sensor
motion_sensor = BinarySensor(motion_settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
motion_sensor.on()

# An additional sensor can be added to the same device, by re-using the DeviceInfo instance previously defined
door_sensor_info = BinarySensorInfo(name="My door sensor", device_class="door", unique_id="my_door_sensor", device=device_info)
door_settings = Settings(mqtt=mqtt_settings, entity=door_sensor_info)

# Instantiate the sensor
door_sensor = BinarySensor(settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
door_sensor.on()

# The two sensors should be visible inside Home Assistant under the device `My device`
```

### Device trigger

The following example creates a device trigger and generates a trigger event:

##### Usage
```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceInfo, DeviceTriggerInfo, DeviceTrigger

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Define the device. At least one of `identifiers` or `connections` must be supplied
device_info = DeviceInfo(name="My device", identifiers="device_id")

# Associate the sensor with the device via the `device` parameter
trigger_info = DeviceTriggerInfo(name="MyTrigger", type="button_press", subtype="button_1", unique_id="my_device_trigger", device=device_info)

settings = Settings(mqtt=mqtt_settings, entity=trigger_info)

# Instantiate the device trigger
mytrigger = DeviceTrigger(settings)

# Generate a device trigger event, publishing an MQTT message that gets picked up by HA
# Optionally include a payload as part of the event
mytrigger.trigger("My custom payload")
```

### Switch

The switch is similar to a _binary sensor_, but in addition to publishing state changes toward HA it can also receive 'commands' from HA that request a state change.
It is possible to act upon reception of this 'command', by defining a `callback` function, as the following example shows:

#### Usage

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the switch
switch_info = SwitchInfo(name="test")

settings = Settings(mqtt=mqtt_settings, entity=switch_info)

# To receive state commands from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    payload = message.payload.decode()
    if payload == "ON":
        turn_my_custom_thing_on()
        # Let HA know that the switch was successfully activated
	my_switch.on()
    elif payload == "OFF":
        turn_my_custom_thing_off()
        # Let HA know that the switch was successfully deactivated
	my_switch.off()

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the switch
my_switch = Switch(settings, my_callback, user_data)

# Set the initial state of the switch, which also makes it discoverable
my_switch.off()

```

### Light

The light is different from other current sensor as it needs its payload encoded/decoded as json.
It is possible to set brightness, effects and the color of the light. Similar to a _switch_ it can
also receive 'commands' from HA that request a state change.
It is possible to act upon reception of this 'command', by defining a `callback` function, as the following example shows:

#### Usage

```py
import json
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Light, LightInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the light
light_info = LightInfo(
    name="test_light",
    brightness=True,
    color_mode=True,
    supported_color_modes=["rgb"],
    effect=True,
    effect_list=["blink", "my_cusom_effect"])

settings = Settings(mqtt=mqtt_settings, entity=light_info)

# To receive state commands from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):

    # Make sure received payload is json
    try:
        payload = json.loads(message.payload.decode())
    except ValueError as error:
        print("Ony JSON schema is supported for light entities!")
        return

    # Parse received dictionary
    if "color" in payload:
        set_color_of_my_light()
        my_light.color("rgb", payload["color"])
    elif "brightness" in payload:
        set_brightness_of_my_light()
        my_light.brightness(payload["brightness"])
    elif "effect" in payload:
        set_effect_of_my_light()
        my_light.effect(payload["effect"])
    elif "state" in payload:
        if payload["state"] == light_info.payload_on:
            turn_on_my_light()
            my_light.on()
        else:
            turn_off_my_light()
            my_light.off()
    else:
        print("Unknown payload")

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the switch
my_light = Light(settings, my_callback, user_data)

# Set the initial state of the light, which also makes it discoverable
my_light.off()

```

### Covers

A cover has five possible states `open`, `closed`, `opening`, `closing` and `stopped`. Most other entities use the states as command payload, but covers differentiate on this. The user HA user can either open, close or stop it in the covers current position.

Covers do not currently support tilt.

A `callback` function is needed in order to parse the commands sent from HA, as the following
example shows:

#### Usage

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Cover, CoverInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the cover
cover_info = CoverInfo(name="test")

settings = Settings(mqtt=mqtt_settings, entity=cover_info)

# To receive state commands from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    payload = message.payload.decode()
    if payload == "OPEN":
	# let HA know that the cover is opening
	my_cover.opening()
	# call function to open cover
        open_my_custom_cover()
        # Let HA know that the cover was opened
	my_cover.open()
    if payload == "CLOSE":
	# let HA know that the cover is closing
	my_cover.closing()
	# call function to close the cover
        close_my_custom_cover()
        # Let HA know that the cover was closed
	my_cover.closed()
    if payload == "STOP":
	# call function to stop the cover
        stop_my_custom_cover()
        # Let HA know that the cover was stopped
	my_cover.stopped()

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the cover
my_cover = Cover(settings, my_callback, user_data)

# Set the initial state of the cover, which also makes it discoverable
my_cover.closed()
```

### Text

The text is an `helper entity`, showing an input field in the HA UI that the user can interact with.
It is possible to act upon reception of the inputted text by defining a `callback` function, as the following example shows:

#### Usage

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Text, TextInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the `text` entity
text_info = TextInfo(name="test")

settings = Settings(mqtt=mqtt_settings, entity=text_info)

# To receive text updates from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    text = message.payload.decode()
    logging.info(f"Received {text} from HA")
    do_some_custom_thing(text)
    # Send an MQTT message to confirm to HA that the text was changed
    my_text.set_text(text)

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the text
my_text = Text(settings, my_callback, user_data)

# Set the initial text displayed in HA UI, publishing an MQTT message that gets picked up by HA
my_text.set_text("Some awesome text")

```

### Number

The number entity is similar to the text entity, but for a numeric value instead of a string.
It is possible to act upon receiving changes in HA by defining a `callback` function, as the following example shows:

#### Usage

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Number, NumberInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the `number` entity.
number_info = NumberInfo(name="test", min=0, max=50, mode="slider", step=5)

settings = Settings(mqtt=mqtt_settings, entity=number_info)

# To receive number updates from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    number = int(message.payload.decode())
    logging.info(f"Received {number} from HA")
    do_some_custom_thing(number)
    # Send an MQTT message to confirm to HA that the number was changed
    my_number.set_value(number)

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the number
my_number = Number(settings, my_callback, user_data)

# Set the initial number displayed in HA UI, publishing an MQTT message that gets picked up by HA
my_number.set_value(42.0)

```

## Contributing

Please run `black` on your code before submitting. There are `git` hooks already configured to run `black` and other checks before every commit, please run `pre-commit install` to enable them.

## Users of ha-mqtt-discoverable

If you use this module for your own project, please add a link here.

- [ha-mqtt-discoverable-cli](https://github.com/unixorn/ha-mqtt-discoverable-cli) - Command line tools that allow using this module from shell scripts

- [plejd-mqtt-ha](https://github.com/ha-enthus1ast/plejd-mqtt-ha) - A containerized Python application that bridges Plejd devices to Home Assistant

## Contributors

<a href="https://github.com/unixorn/ha-mqtt-discoverable/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=unixorn/ha-mqtt-discoverable" />
</a>

Made with [contributors-img](https://contributors-img.web.app).
