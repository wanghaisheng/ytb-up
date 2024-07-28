#!/bin/sh

set -eu
folder_path="./.venv"

# 检查文件夹是否存在
if [ -d "$folder_path" ]; then
    echo "you have set it up before"
    source .venv/Scripts/activate
    python -m pip install -r requirements.txt
    # python  setup.py install
    python -m pip install build
    folder_path='./build'
    if [ -d "$folder_path" ]; then

        rm -r build/
    fi
    folder_path="./dist"

    if [ -d "$folder_path" ]; then

        rm -r dist/
    fi
    python -m build --wheel
    python -m pip uninstall -y tsup
    python -m pip install dist/tsup-*.whl

else
    echo "it is a fresh start"
    python -m venv --upgrade-deps .venv
    source .venv/Scripts/activate
    python -m pip install -r requirements.txt
    python -m pip install build
    folder_path='./build'
    if [ -d "$folder_path" ]; then

        rm -r build/
    fi
    folder_path="./dist"

    if [ -d "$folder_path" ]; then

        rm -r dist/
    fi
    python -m build --wheel
    python -m pip install dist/tsup-*.whl

fi

python examples/youtube/onefile-example_youtube_windows.py

