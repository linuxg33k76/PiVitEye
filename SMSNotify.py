# SMSNotify Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date: August 7, 2016 v1.0.0
# Revision: August 21, 2016 v1.0.1
# Revision: August 21, 2016 v1.1.0 - Added Security for TwilioSMS via /etc/piviteye/twilio.conf file

# This program sends out an SMS message for motion detected by webcam

# Import class files

import os
import glob
import twclass
import json


def main():

    path = '/mnt/usb/video/'
    latest_video = max(glob.iglob(os.path.join(path, '*.[Aa][Vv][Ii]')), key=os.path.getctime)
    msg = 'Motion Detected!  Recording has been made: ' + latest_video

    #  Load Twilio Configuration VALUES
    with open('/etc/piviteye/twilio.conf') as data_file:
        data = json.load(data_file)
    data_file.close()

    #  New TwilioSMS instance
    tw = twclass.TwilioSMS(data['tw_account'],
                           data['tw_token'],
                           data['tw_receiver'],
                           data['tw_sender'])

    # Call send_message method
    tw.send_message(msg)

if __name__ == "__main__":
    main()
