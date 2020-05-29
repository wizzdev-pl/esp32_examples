#!/bin/bash

set -e

USERDIR=$(pwd)
BASEDIR=$(dirname "$0")

cd "$BASEDIR"
cd ./../  # In MicroPython dir

if source venv/bin/activate ; then
    echo "Installing requirements..."
    pip3 install wheel
    pip3 install -r requirements.txt
else
    echo "Creating virtual environment"
    python3 -m venv venv
    source ./venv/bin/activate
    echo "Installing requirements..."
    pip3 install wheel
    pip3 install -r requirements.txt
fi

cd "$USERDIR"

echo "Done."
