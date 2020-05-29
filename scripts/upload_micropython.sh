#!/bin/bash

set -e

PORT=/dev/ttyUSB0
if [ "$1" != "" ]; then
    echo "Writing to Port" + "$1"
    PORT = "$1"
else
    echo "No port specified. Using default: /dev/ttyUSB0"
fi

read -n 1 -s -r -p "Reset ESP32 into bootloader mode - Hold BOOT button and click EN button. Release BOOT. Then press any key to continue"
echo "Erasing Chip..."
esptool.py --chip esp32 --port "$PORT" erase_flash || exit 1
echo "Flashing MicroPython firmware..."
esptool.py --chip esp32 --port "$PORT" --baud 230400 write_flash -z 0x1000 MicroPython_firmware/esp32-idf3-20191220-v1.12.bin --verify
echo "Done."

