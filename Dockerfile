FROM python:3.10-slim

ARG application_version
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

COPY dist/ha_mqtt_discoverable-${application_version#v}-py3-none-any.whl /tmp/

SHELL ["/bin/bash", "-c"]
RUN python -m pip install --no-cache-dir /tmp/ha_mqtt_discoverable-${application_version:1}-py3-none-any.whl

USER nobody

CMD ["bash", "-l"]
