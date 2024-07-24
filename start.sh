#!/bin/sh

set -eu

python3 -m venv --upgrade-deps .venv
.venv/bin/python3 -m pip install -U --disable-pip-version-check --editable .[non-termux]
.venv/bin/python3 examples/onefile-example_youtube_windows.py

