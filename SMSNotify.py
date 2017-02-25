#SMSNotify Python Program for Raspberry Pi 3
#Author:  Ben Calvert
#Date: August 7, 2016 v1.0.0
#Revision: August 21, 2016 v1.0.1

#This program sends out an SMS message for motion detected by webcam

#Import class files

import os
import glob
import twclass

def main():
    
    path = '/mnt/usb/video/'
    latest_video = max(glob.iglob(os.path.join(path, '*.[Aa][Vv][Ii]')), key=os.path.getctime)
    msg = 'Motion Detected!  Recording has been made: ' + latest_video
    #Instantiate the class
    tw = twclass.TwilioSMS()
    #Call send_message method
    tw.send_message(msg)
    
if __name__ == "__main__":
    main()