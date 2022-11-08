FROM unixorn/debian-py3:latest
ARG application_version="0.3.0"
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

RUN apt-get update && \
    apt-get install -y apt-utils ca-certificates --no-install-recommends && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/* && \
    /usr/bin/python3 -m pip install --upgrade pip --no-cache-dir && \
    pip3 install --no-cache-dir ha-mqtt-discoverable && \
    pip3 cache purge

CMD ["bash", "-l"]
