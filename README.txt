PiVitEye Python Program

###REQUIRES###
1.  Raspberry Pi 3
2.  USB Webcam
3.  External Speaker

###Linux Packages to Install###
1.  motion
2.  fswebcam
3.  setup raspberry pi audio - sudo raspi-config
4.  Twilio for python - via pip
5.  sudo apt-get install python3-flask
6.  camera (pip3 install camera)

All files can live where you place the contents of this repo.  Just make sure of the following:

1.  Pathing is correct.
2.  Permissions for users are correct.  Your Raspberry Pi account 'pi' and 'motion' will need access to 
    /dev/snd and it's contents.  You will need to add 'audio' as a group to both pi and motion.
    usermod -a -G audio <user> - you can find permission information online.
3.  If things don't work, be sure to verify paths and permissions!
4.  Symbolic Link to external storage on raspberry pi in the ../webapp/static/ directory