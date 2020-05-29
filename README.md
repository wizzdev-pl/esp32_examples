# ESP32 WizzDev wireless comunication examples #
 
## Overview

This repository contains variouse examples of ESP32 MCU wireless comunication in micropython

## Prerequisites ###
All instructions were tested under Ubuntu 18.04 and ESP-wroom-32
Before starting instruction you require
- python3.6-dev
- python3.6-venv
- python3-pip
- user added to dialout greoup

## Getting the repo
    Add links from bitbucket

## Environment setup
To setup python enviornment with required tools use:
```
cd <repo directory>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Uploading the firmware to MCU
Connect your ESP to usb port if uploading fails try another port
Activate virtual enviorment and run following commands:
```
source venv/bin/activate
./scripts/upload_micropython.sh
python3 scripts/upload_scripts.py

```
You need to upload micropython only once. After uploading scripts to esp32 press "EN" button.

## Displaying output from micropython
To display output from esp32 serial port run command:
```
picocom /dev/ttyUSB0 --baud 115200

```
Your esp32 might be connected on diffrent port when you use serial usb devices. 
To exit picocom use ctrl+a and ctrl+x commands 


The latest Micropython version is available at [https://micropython.org/download#esp32](https://micropython.org/download#esp32)
For May of 2020, it is recommended to use newest stable IDF3 MicroPython version, but it may be better to use IDF4 in the future.

While powering on, the microPython on the ESP will first execute 'boot.py' file. 

For More info go to [https://docs.micropython.org/en/latest/esp32/quickref.html#](https://docs.micropython.org/en/latest/esp32/quickref.html#)
