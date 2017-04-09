#!/bin/bash

#Cache Log files daily

date=$(date +%m-%d-%Y)

cp /mnt/usb/log/piviteye.log /mnt/usb/log/piviteye-$date.log

# Refresh logfile
echo "Beginning Log..." > /mnt/usb/log/piviteye.log
