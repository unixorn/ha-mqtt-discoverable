.PHONY: c clean \
	f format \
	h help \
	fatimage \
	local \
	publish \
	t test \
	wheel

h: help
c: clean
f: format
t: test

help:
	@echo "Options:"
	@echo "format: Reformat all python files with black"
	@echo "tests: Run tests with nosetest"
	@echo "verbose_tests: Run tests with nosetest -v"

clean:
	rm -fv dist/*.tar dist/*.whl

format:
	poetry run black ha_mqtt_discoverable/*.py \
		ha_mqtt_discoverable/*/*.py \
		tests/*.py
test:
	nosestests -v

local: wheel requirements.txt
	docker buildx build --load -t unixorn/ha-mqtt-discoverable-test -f Dockerfile.testing .

fatimage: wheel
	docker buildx build --platform linux/arm64,linux/amd64 --push -t unixorn/ha-mqtt-discoverable .
	make local

wheel: clean format
	poetry build

publish: fatimage
	poetry publish

# We only use this to enable the Dockerfile.testing have a layer for the python
# dependencies so we don't have to reinstall every time we test a new change
requirements.txt: poetry.lock pyproject.toml Makefile
	poetry export -o requirements.txt
