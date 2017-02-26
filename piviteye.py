#Piviteye Python Program for Raspberry Pi 3
#Author:  Ben Calvert
#Date:  May 27, 2016 v1.0.0
#Revision:  June 21, 2016 v1.0.9
#Revision:  August 6, 2016 v1.0.10 - enhancements
#Revision:  August 7, 2016 v1.1.0 - added twclass.py dependency
#Revision:  October 25, 2016 v1.3.0 - code cleanup and usb storage added
#Revision:  February 25, 2017 v1.5.0 - added /etc/piviteye/twilio.conf JSON config file code
#Revision:  February 25, 2017 v1.5.0 - added status command uptime message

#This program takes SMS messages and initiates actions based on command Rx'd

#Import class files
from gpiozero import LED,Button

from time import sleep
from twilio.rest import TwilioRestClient
import twclass
import piviteyedb
import picamclass
import programlogclass
import subprocess
import datetime
import json


#Define command check

def command_check():
    while (True):
            #get old message
            old_msg_id = tw.get_last_msg()
            old_msg = tw.get_last_msg_body().lower().strip()
            logger.log_it('Last Rx Message ID -> ' + old_msg_id)
            logger.log_it('Last Rx Message    -> ' + old_msg)

            logger.log_it('Sleeping for 15 seconds zzz...')
            time = datetime.datetime.now()
            sleep(15)

            logger.log_it('Waiting for New Command...')
            messages = tw.get_messages()

            #remove whitespaces from begining or end of the last message's body
            msg = messages[0].body.lower().strip()

            #store last message's sid number (ID number)
            msg_num = messages[0].sid
            logger.log_it('New Rx Message ID -> ' + msg_num)

            #check message status and pull recieved messages only
            if messages[0].status == 'received' and msg_num != old_msg_id:

                #store the new message sid to Global Variable old_msg, so we don't reissue this command
                #old_msg = msg_num
                #log message in logfile
                logger.log_it('Command was --> '+ msg)

                #look up command in database (piviteye.db)
                command = db.get_command(msg)
                if command != []:
                    logger.log_it(command[2])
                    tw.send_message(command[3])
                    if command[4] != "":
                        pi_command(command[4])
                    else:
                        pass
                    if command[5] != "":
                        cmd_response = subprocess.call(command[5],shell=True)
                        if cmd_response == 0:
                            tw.send_message('Command Completed Successfully!')
                        else:
                            tw.send_message('Command failed... :(')
                    else:
                        pass
                else:
                    logger.log_it('Invalid Command Received.')
                    tw.send_message('Invalid Command Received.')
            else:
                pass

#Define Pi Command

def pi_command(command):
    if command == "halt":
        graceful_exit()
    elif command == "pivideo":
        v = picamclass.PiCam()
        v.take_video(0)
    elif command == "garage_door":
        toggle_relay()
    elif command == "status":
        # Use the global program start time to calculate
        prog_uptime = datetime.datetime.now() - start_time
        message = 'Program Uptime: {0}'.format(str(prog_uptime))
        tw.send_message(message)
    elif command == 'uptime':
        # Get command output and convert byte code to utf-8
        message = subprocess.check_output('uptime')
        tw.send_message(str(message,'utf-8'))
    else:
        return


#Define Quit Function

def graceful_exit():
    logger.log_warn('User Initiated Exit')
    logger.log_it('Gracefully Exiting Program.')
    tw.send_message('User Initiated Shutdown of System Complete.')
    raise SystemExit('User Initiated Exit')

def toggle_relay():
    # Rework This...
    open_led.on()
    closed_led.on()
    sleep(2)
    open_led.off()
    closed_led.off()

#----------------------Initialize------------------------#

def main():

    #loop continuing to get messages every 30 seconds
    #If exit_code == True, call the graceful_exit() function

    while (True):
        command_check()

# Start Point

if __name__ == "__main__":

    # # GPIO Object Instances
    # closed_led = LED(4)         #Red LED on GPIO port 4
    # open_led = LED(17)          #Green LED on GPIO port 17
    # button = Button(23)         #Button on GPIO port 23

    # Load Twilio Configuration VALUES
    with open ('/etc/piviteye/twilio.conf') as data_file:
        data = json.load(data_file)

    # New TwilioSMS instance
    tw = twclass.TwilioSMS(data['tw_account'],data['tw_token'],data['tw_receiver'],data['tw_sender'])

    # New Logger instance
    logger = programlogclass.ProgramLog()

    # New piviteye database instance
    db = piviteyedb.PyVitEyeDB()

    # # LED Test
    # open_led.on()
    # closed_led.on()
    # sleep(2)                #Sleep 2 seconds
    # open_led.off()
    # closed_led.off()

    # Initialization SMS message
    logger.log_it('Starting Program...')
    tw.send_message('Piviteye Program Initalized.')
    start_time = datetime.datetime.now()
    #Call Main()
    main()
