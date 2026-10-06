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

from collections.abc import Callable

import pytest
from paho.mqtt.client import Client
from pytest_mock import MockerFixture

from ha_mqtt_discoverable import Discoverable, EntityInfo, Settings
from ha_mqtt_discoverable.sensors import (
    ButtonInfo,
    CoverInfo,
    LightInfo,
    LockInfo,
    NumberInfo,
    SelectInfo,
    SwitchInfo,
    TextInfo,
    ValveInfo,
)


@pytest.mark.parametrize(
    "info_class",
    [
        ButtonInfo,
        CoverInfo,
        LightInfo,
        LockInfo,
        NumberInfo,
        SelectInfo,
        SwitchInfo,
        TextInfo,
        ValveInfo,
    ],
)
@pytest.mark.parametrize("retain", [True, False])
def test_retain_is_included_in_discovery_payload(
    mocker: MockerFixture,
    info_class: Callable[..., EntityInfo],
    retain: bool,
):
    mqtt_client = mocker.Mock(spec=Client)
    entity = info_class(name="test", retain=retain)
    settings = Settings(mqtt=Settings.MQTT(client=mqtt_client), entity=entity)

    config = Discoverable[EntityInfo](settings).generate_config()

    assert config["retain"] is retain
