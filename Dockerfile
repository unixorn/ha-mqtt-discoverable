FROM python:3.10-slim

ARG application_version
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

SHELL ["/bin/bash", "-c"]
RUN python -m pip install --no-cache-dir ha-mqtt-discoverable==${application_version:1}

USER nobody

CMD ["bash", "-l"]
