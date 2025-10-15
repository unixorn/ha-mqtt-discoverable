# Availability Management

This library can publish availability so Home Assistant (HA) knows whether an entity is online or offline. When `manual_availability` is enabled, a retained Last Will and Testament (LWT) is configured and you are responsible for marking the entity online when ready.

## Quick start

```py
from ha_mqtt_discoverable import Settings, EntityInfo, Discoverable

mqtt_settings = Settings.MQTT(host="localhost")
entity_info = EntityInfo(name="test", component="binary_sensor")
settings = Settings(mqtt=mqtt_settings, entity=entity_info, manual_availability=True)

d = Discoverable(settings)

# After your entity is ready, set availability to online
d.set_availability(True)

# Later, if it becomes unavailable
d.set_availability(False)
```

## Topics and payloads

- Availability topic (retained): `hmd/<component>/<device?>/<name>/availability`
- Payloads: `online` when available, `offline` when not available
- QoS: recommend 1

When `manual_availability=True`:
- The client will register an LWT with payload `offline` retained.
- After initialization, publish `online` retained using `set_availability(True)`.

## Multiple entities per device

Prefer a single availability lifecycle per physical device. If multiple entities share a lifecycle, keep them consistent by toggling availability for all related entities at the same time.

## Troubleshooting

- HA shows entity as unavailable after restart: ensure availability messages are retained.
- Availability topic mismatch: confirm the topic in the discovery config matches the one you publish to.
- Payload case: use exactly `online`/`offline`.

## Best practices

- Keep availability payloads small (e.g., `online`/`offline`).
- Use retained messages so state survives restarts.
- Re-assert `online` after reconnects.

