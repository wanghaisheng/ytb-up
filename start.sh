#!/bin/sh

set -eu

python -m venv --upgrade-deps .venv
source .venv/Scripts/activate

python -m pip install -r requirements.txt
python  setup.py install
python examples/onefile-example_youtube_windows.py

