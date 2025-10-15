"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import time
from threading import Event

from paho.mqtt import publish

from ha_mqtt_discoverable import EntityInfo, Settings, Subscriber


def test_callbacks_multiple_entities_fire_independently():
    mqtt_settings = Settings.MQTT(host="localhost")

    a_info = EntityInfo(name="sensor_a", component="text")
    b_info = EntityInfo(name="sensor_b", component="text")

    events = []
    a_event = Event()
    b_event = Event()

    def cb_a(_, __, message):
        events.append(("a", message.payload.decode()))
        a_event.set()

    def cb_b(_, __, message):
        events.append(("b", message.payload.decode()))
        b_event.set()

    a = Subscriber(Settings(mqtt=mqtt_settings, entity=a_info), cb_a)
    b = Subscriber(Settings(mqtt=mqtt_settings, entity=b_info), cb_b)

    time.sleep(2)

    publish.single(a._command_topic, "one", hostname="localhost")
    publish.single(b._command_topic, "two", hostname="localhost")

    assert a_event.wait(3)
    assert b_event.wait(3)
    logging.info("events=%s", events)
    assert ("a", "one") in events
    assert ("b", "two") in events
