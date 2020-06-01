# ESP32 WizzDev wireless comunication examples #
 
## Overview

This repository contains various examples of ESP32 MCU wireless communication in MicroPython

## Prerequisites ###
All instructions were tested under Ubuntu 18.04 and ESP-Wroom-32
Before starting, you will need:
- python3.6-dev
- python3.6-venv
- python3-pip
- user added to dialout group

## Getting this repository
    Add links from bitbucket

## Environment setup
To setup python environment with required tools use:
```
cd <repo directory>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Uploading the firmware to MCU
Connect your ESP to usb port if uploading fails try another port.

Activate virtual environment and run following commands:
```
source venv/bin/activate
./scripts/upload_micropython.sh
python3 scripts/upload_scripts.py

```
You need to upload MicroPython firmware only once. After uploading scripts to esp32 press "EN" button.

## Displaying output from MicroPython
To display output from esp32 serial port run command:
```
picocom /dev/ttyUSB0 --baud 115200

```
Your esp32 might be connected on different port when you use serial usb devices. 
To exit picocom use ctrl+a and ctrl+x commands 


The latest Micropython version is available at [https://micropython.org/download#esp32](https://micropython.org/download#esp32)
For May of 2020, it is recommended to use newest stable IDF3 MicroPython version, but it may be better to use IDF4 in the future.

While powering on, the MicroPython on the ESP will first execute 'boot.py' file. 

For More info go to [https://docs.micropython.org/en/latest/esp32/quickref.html#](https://docs.micropython.org/en/latest/esp32/quickref.html#)
