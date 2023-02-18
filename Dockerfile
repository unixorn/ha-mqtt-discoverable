FROM python:3.10

ARG application_version="0.3.0"
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

RUN apt-get update && \
    apt-get install -y apt-utils=2.2.4 ca-certificates=20210119 --no-install-recommends && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/* && \
    pip install --no-cache-dir ha-mqtt-discoverable==${application_version} && \
    pip cache purge

USER nobody

CMD ["bash", "-l"]
