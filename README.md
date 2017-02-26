# piviteye
Raspberry Pi Home Monitor &amp; Utility Project

Still pending licensing decision.

Software created by Ben Calvert (linuxg33k76@gmail.com)

This software requires:

1.  TwilioSMS for Python (pip3 install twilio) & your own Twilio account/token
    - Twilio's SMS API is a paid for service, Just FYI.
2.  /etc/piviteye/twilio.conf file in JSON format
3.  sudo apt-get install motion - configure via /etc/motion/motion.conf (autostart is your option)
4.  sudo apt-get install tshark (packet capture functions)
4.  Hardware:  Raspberry Pi 3

Installation
1.  I installed to /opt/piviteye
2.  Make sure you have python3 and the all necessary pip packages installed
3.  Add /etc/piviteye directory and include a JSON fomatted text file as shown below
{"tw_account":<account>,"tw_token":<token>,"tw_receiver":<your SMS number>,"tw_sender":<twilio SMS number>}

