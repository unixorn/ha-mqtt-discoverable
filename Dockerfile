FROM python:slim

ARG application_version
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

# hadolint ignore=DL3013
RUN python -m pip install --no-cache-dir ha-mqtt-discoverable

USER nobody

CMD ["bash", "-l"]
