#!/bin/bash

#create a date variable coded with Year, month, day, Hour and Minute

DATE=$(date +"%Y-%m-%d_%H_%M")

# tshark command 
sudo tshark -i eth0 -a duration:60 -b filesize:2048 -w /mnt/usb/pcap/output_$DATE.pcap -F pcap
