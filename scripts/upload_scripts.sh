#!/bin/bash

set -e

PORT=/dev/ttyUSB0
if [ "$1" != "" ]; then
    echo "Writing to Port" + "$1"
    PORT = "$1"
else
    echo "No port specified. Using default: /dev/ttyUSB0"
fi

if python3 -V | grep -q "3.6"; then
  echo "Python 3.6 detected!"
else
  echo "No Python 3.6 detected!"
  exit 1
fi

if python scripts/create_default_config.py; then
    echo "Fill config with proper data and rerun 'uplaod_scripts.sh' or 'upload_all.sh' script"
    exit 0
fi

DIR="$(cd "$(dirname "$0")" && pwd)"
python3 $DIR/upload_scripts.py


echo "Done."
