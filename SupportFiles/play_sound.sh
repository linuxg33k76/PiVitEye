#!/bin/bash

#Set output to max volume (This will scare that darn cat!)
sudo amixer cset numid=1 -- 100%

#Play wavefile
aplay /opt/piviteye/SupportFiles/bank_alarm_3.wav
