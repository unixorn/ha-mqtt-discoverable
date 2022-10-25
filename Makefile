.PHONY: c clean f format h help

h: help

help:
	@echo "Options:"
	@echo "format: Reformat all python files with black"
	@echo "tests: Run tests with nosetest"
	@echo "verbose_tests: Run tests with nosetest -v"

c: clean
f: format

clean:
	rm -fv dist/*.tar dist/*.whl

format:
	poetry run black hass_mqtt_devices/*.py \
		hass_mqtt_devices/*/*.py \
		tests/*.py
test:
	nosestests -v

local: wheel
	docker buildx build --load -t unixorn/hass-mqtt-devices-test -f Dockerfile.testing .

fatimage: wheel
	docker buildx build --platform linux/arm64,linux/amd64 --push -t unixorn/hass-mqtt-devices .
	make local

wheel: clean format requirements.txt
	poetry build

publish: fatimage
	poetry publish

requirements.txt: poetry.lock Makefile
	poetry export -o requirements.txt
