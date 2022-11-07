FROM unixorn/debian-py3:latest
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"

RUN apt-get update && \
    apt-get install -y apt-utils ca-certificates --no-install-recommends && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/* && \
    /usr/bin/python3 -m pip install --upgrade pip --no-cache-dir && \
    pip3 install --no-cache-dir ha_mqtt_discoverable && \
    pip3 cache purge

CMD ["bash", "-l"]
