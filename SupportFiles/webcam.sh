#!/bin/bash

#create a date variable coded with Year, month, day, Hour and Minute

DATE=$(date +"%Y-%m-%d_%H_%M")

# Use the ffmpeg replacement (avconv - installed with libav-tools) and pull 60 seconds of
# raw video from /dev/video0 (webcam) and store to a .webm file

avconv -f video4linux2 -framerate 30 -t 60 -video_size 1280x720 -i /dev/video0 -y /mnt/usb/video/user_initiated_$DATE.webm
