SHELL := /bin/bash
PYTHON = python3
POETRY = poetry
TEST_PATH = ./tests/
FLAKE8_EXCLUDE = venv,.venv,.eggs,.tox,.git,__pycache__,*.pyc,clip.py

.PHONY: install
install:
	${POETRY} install

.PHONY: check
check:
	${PYTHON} -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude ${FLAKE8_EXCLUDE}
	${PYTHON} -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=70 --statistics --exclude ${FLAKE8_EXCLUDE}

.PHONY: clean
clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

.PHONY: build
build:
	${POETRY} build

.PHONY: publish
publish:
	${POETRY} publish

.PHONY: test
test:
	poetry run pytest -s -v
