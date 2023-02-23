FROM python:3.10

ARG application_version
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="ha-mqtt-discoverable utility image"
LABEL version=${application_version}

RUN apt-get update && \
    apt-get install -y apt-utils=2.2.4 ca-certificates=20210119 --no-install-recommends && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/*

# Copy wheel file built by Poetry
COPY dist/*.whl /app/

RUN python -m pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir /app/*.whl && \
    pip cache purge && \
    rm -rf /app/*.whl

USER nobody

CMD ["bash", "-l"]
