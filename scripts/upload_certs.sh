#!/bin/bash

set -e

PORT=/dev/ttyUSB0
if [ "$1" != "" ]; then
    echo "Writing to Port" + "$1"
    PORT = "$1"
else
    echo "No port specified. Using default: /dev/ttyUSB0"
fi

if ampy --port /dev/ttyUSB0 ls | grep -q "cert"; then
  echo "/cert/ directory already exists on the device."
else
  echo "  Creating directory /cer/"
  ampy --port "$PORT" mkdir cert
fi

echo "Uploading device cert..."
ampy --port "$PORT" put cert/cert.crt cert/cert.crt
echo "Uploading private key..."
ampy --port "$PORT" put cert/priv.key cert/priv.key
#echo "Uploading ca_cert key..."
#ampy --port "$PORT" put cert/cacert.pem cert/cacert.pem
echo "Done"
