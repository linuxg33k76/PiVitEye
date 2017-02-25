#!/bin/bash

#create a date variable coded with Year, month, day, Hour and Minute

DATE=$(date +"%Y-%m-%d_%H:%M")

#Issue the fswebcam command and store the picture in /home/pi/webcam with the proper file name
#based on the variable above.

fswebcam -r 1280x720 --top-banner   /mnt/usb/video/$DATE.jpg
