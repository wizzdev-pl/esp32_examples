#!/bin/bash

set -e

PORT=/dev/ttyUSB0
if [ "$1" != "" ]; then
    echo "Writing to Port" + "$1"
    PORT = "$1"
else
    echo "No port specified. Using default: /dev/ttyUSB0"
fi

echo "Uploading config.json..."
ampy --port "$PORT" put src/config.json || exit 1
