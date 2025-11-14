# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/unixorn/ha-mqtt-discoverable/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                   |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| ha\_mqtt\_discoverable/\_\_init\_\_.py |      216 |       30 |       50 |       10 |     82% |232-236, 242-246, 254-268, 272, 286, 310-311, 329-333, 369-370, 394->exit, 427, 439-448 |
| ha\_mqtt\_discoverable/sensors.py      |      326 |        0 |       42 |        0 |    100% |           |
| ha\_mqtt\_discoverable/utils.py        |        9 |        3 |        0 |        0 |     67% |     40-42 |
| tests/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_binary\_sensor.py          |       26 |        0 |        2 |        1 |     96% |  43->exit |
| tests/test\_button.py                  |       15 |        4 |        0 |        0 |     73% |     24-28 |
| tests/test\_camera.py                  |       23 |        0 |        0 |        0 |    100% |           |
| tests/test\_cover.py                   |       25 |        0 |        0 |        0 |    100% |           |
| tests/test\_device\_trigger.py         |       22 |        0 |        0 |        0 |    100% |           |
| tests/test\_discoverable.py            |      187 |        2 |        2 |        1 |     98% |   223-224 |
| tests/test\_image.py                   |       67 |        0 |        8 |        4 |     95% |74->exit, 82->84, 84->86, 86->exit |
| tests/test\_light.py                   |       53 |        0 |        0 |        0 |    100% |           |
| tests/test\_lock.py                    |       35 |        0 |        0 |        0 |    100% |           |
| tests/test\_number.py                  |       23 |        0 |        0 |        0 |    100% |           |
| tests/test\_select.py                  |       25 |        0 |        0 |        0 |    100% |           |
| tests/test\_sensor.py                  |       54 |        0 |        0 |        0 |    100% |           |
| tests/test\_subscriber.py              |       38 |        0 |        0 |        0 |    100% |           |
| tests/test\_switch.py                  |       18 |        0 |        0 |        0 |    100% |           |
| tests/test\_text.py                    |       28 |        0 |        0 |        0 |    100% |           |
|                              **TOTAL** | **1190** |   **39** |  **104** |   **16** | **95%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/unixorn/ha-mqtt-discoverable/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/unixorn/ha-mqtt-discoverable/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/unixorn/ha-mqtt-discoverable/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/unixorn/ha-mqtt-discoverable/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Funixorn%2Fha-mqtt-discoverable%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/unixorn/ha-mqtt-discoverable/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.