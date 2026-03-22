FROM python:slim

ARG application_version
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

RUN python -m pip install --no-cache-dir ha-mqtt-discoverable==${application_version}

USER nobody

CMD ["bash", "-l"]
