#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H:%M")

#sleep for a minute to allow everything to load
sleep 60

#Start Python program

python3 /opt/piviteye/piviteye.py >> /mnt/usb/log/PiVitEye_$DATE.log
