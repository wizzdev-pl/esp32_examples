#!/bin/bash

set -e

USERDIR=$(pwd)
BASEDIR=$(dirname "$0")

cd "$BASEDIR"
cd ./../  # In MicroPython dir

if [[ "$VIRTUAL_ENV" != "" ]]; then  # TODO: Better solution to check if is in venv
  INVENV=1
else
  INVENV=0
fi

if test "$INVENV" ; then
  echo "Already in venv"
else
  if source ./venv/bin/activate; then
    echo "Entered virtual env"
  else
    echo "Virtual env not found. Use setup.sh script or create new environment manually!"
    exit 2
  fi
fi

if python3 scripts/create_default_config.py; then
    echo "Created new config file at MicroPython/src/config.json"
    echo "Fields that need to be filled for minimum viable configuration are: ssid, password ..."
    echo "...for use with local MQTT broker: local_endpoint, client_id, topic"
    echo "...for use with AWS: aws_endpoint, client_id, topic, use_aws"
    echo "Fill config with proper data and rerun 'uplaod_all.sh' script"
    exit 0
fi

echo "Uploading MicroPython..."
scripts/upload_micropython.sh
sleep 1 # Wait for ESP32 serial to reset
echo "Uploading Script files..."
scripts/upload_scripts.sh

if test -f "cert/cacert.pem" && test -f "cert/priv.key" && test -f "cert/cert.crt"; then
    echo "Uploading Certificates..."
    scripts/upload_certs.sh
else
    echo "No certificates fount in ./cert/"
    echo "No certificates will be uploaded"
fi

esptool.py --chip esp32 --before default_reset run

cd "$USERDIR"
