# Contributing

## Setup

ha-mqtt-discovery uses [poetry](https://python-poetry.org/) to manage module dependencies and make packaging the module easier. Once you install `poetry`, run `poetry install` to have it create a venv for you to use during development.

We use [Autohook](https://github.com/Autohook/Autohook) to run our pre-commit/postcheckout etc `git` hooks.  Please run `hooks/autohook.sh install` at the root of the repository to enable autohook to handle the `git` pre-commit and post-checkout scripts. This won't affect any of your other repositories, just this one. The `git` scripts take care of some cleanups of stray `.pyc` and `.pyo` files, and then run `black` on the `.py` files in your commit.

## Contribution Guidelines

- PRs should include readme updates for any added/changed/removed functionality.
- The current state of tests in the repo is frankly terrible. [issues/20](https://github.com/unixorn/ha-mqtt-discovery/issues/20) to backfill tests is already going to be a lot of work, so please add pytest tests for any new functions you add to keep from piling on more.
- Please use `pydantic` to validate input settings and provide default values.

## Linting the project files

This project uses [Megalinter](https://megalinter.io/latest/) to check the codebase automatically using Github Actions.
It is also possible to run the linter locally to better understand the problems and check the code before a commit.
You can use the [mega-linter-runner](https://megalinter.io/latest/mega-linter-runner/#installation), if you have `Node` and `Docker` locally available.

To run all the linters as configured in the `.mega-linter.yml` file, use:

```bash
npx mega-linter-runner --flavor python
```

It will print out the results in the console, as well as generate a `megalinter-reports` directory with all its reports.
