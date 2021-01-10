
# Piviteye Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date:  May 27, 2016 v1.0.0
# Revision:  May 30, 2018 v1.2.1

# This program takes SMS messages and initiates actions based on command Rx'd

# Import class files

# from gpiozero import LED, Button
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import datetime
import json
from Classes import twclass
from Classes import piviteyedb as Pdb
from Classes import picamclass
from Classes import programlogclass

# Define Pi Command


def pi_command(command, vars):
    if command == "halt":
        graceful_exit()
    elif command == "pivideo":
        v = picamclass.PiCam()
        v.take_video(0)
    elif command == "relay1_toggle":
        # Toggle GPIO Point 14 check integer version of vars for user provided delay
        if vars != '' and int(vars) > 0:
            activateRelay(14, int(vars))
        else:
            # Default 2 seconds
            activateRelay(14, 2)
    elif command == "relay2_toggle":
        # Toggle GPIO Point 15 check integer version of vars for user provided delay
        if vars != '' and int(vars) > 0:
            activateRelay(15, int(vars))
        else:
            # Default 2 seconds
            activateRelay(15, 2)
    elif command == "status":
        # Use the global program start time to calculate
        prog_uptime = datetime.datetime.now() - start_time
        message = 'Program Uptime: {0}'.format(str(prog_uptime))
        tw.send_message(message)
    elif command == 'uptime':
        # Get command output and convert byte code to utf-8
        message = subprocess.check_output('uptime')
        tw.send_message(str(message, 'utf-8'))
    else:
        return

# Define Quit Function


def graceful_exit():
    logger.log_warn('User Initiated Exit')
    logger.log_it('Gracefully Exiting Program.')
    tw.send_message('User Initiated Shutdown of System Complete.')
    raise SystemExit('User Initiated Exit')

# Define Toggle Relay Function


# def toggle_relay():
#     # # GPIO Object Instances
#     relay = LED(14)
#     relay.off()
#     sleep(3)
#     relay.on()

def activateRelay(pin, seconds=3):
    
    # Activate designated Relay for # Seconds

    GPIO.output(pin, False)
    sleep(seconds)
    GPIO.output(pin, True)

# ----------------------Initialize------------------------ #


def main():

    # loop continuing to get messages every 15 seconds
    # If exit_code == True, call the graceful_exit() function

    while True:

        # Daily Program Status Notification Check
        date_string = datetime.datetime.now().strftime('%H:%M')
        if date_string == '20:30':

            try:
                tw.send_message(('The current Time is: {0}.  I am Still Alive!').format(date_string))
            except:
                logger.log_it('Unable to send message at 20:30 hours.')

            sleep(60)

        # get old message

        try:
            old_msg_id = tw.get_last_msg()
            old_msg = tw.get_last_msg_body().lower().strip()
            logger.log_it('Last Rx Message ID -> ' + old_msg_id)
            logger.log_it('Last Rx Message    -> ' + old_msg)

            logger.log_it('Sleeping for 15 seconds zzz...')
            time = datetime.datetime.now()
            sleep(15)

            logger.log_it('Waiting for New Command...')
            messages = tw.get_messages()

            # remove whitespaces from begining or end of the last message's body
            msg = messages[0].body.lower().split(" ")[0]
            msg_vars = messages[0].body.split(" ")[1]
            # print(msg, msg_vars) # For testing purposes
 

            # store last message's sid number (ID number)
            msg_num = messages[0].sid
            logger.log_it('Rx Message ID -> ' + msg_num)
        except:
            logger.log_it('Unable to process message.')

        # check message status and pull recieved messages only
        if messages[0].status == 'received' and msg_num != old_msg_id:

            # log message in logfile
            logger.log_it('Command was --> ' + msg)

            # look up command in database (piviteye.db)
            command = Pdb.get_command(msg)
            if command != []:
                logger.log_it(command.logmsg)
                if msg_vars !='' and 'relay' in msg:
                    tw.send_message((command.smsmsg + ' with variable {0} seconds').format(msg_vars))
                else:
                    tw.send_message(command.smsmsg)
                if command.picmd != '':
                    pi_command(command.picmd, msg_vars)

                if command.subcall != "":
                    cmd_response = subprocess.call(command.subcall, shell=True)
                    if cmd_response == 0:
                        tw.send_message('Command Completed Successfully!')
                    else:
                        tw.send_message(('Command failed with code: {0}... :(').format(str(cmd_response)))
            else:
                logger.log_it('Invalid Command Received.')
                tw.send_message('Invalid Command Received.')

# Program Start Point

if __name__ == "__main__":

    # Load Twilio Configuration VALUES
    with open('/etc/piviteye/twilio.conf') as data_file:
        data = json.load(data_file)
    data_file.close()

    # New TwilioSMS instance
    tw = twclass.TwilioSMS(data)

    # New Logger instance
    logger = programlogclass.ProgramLog()

    # New piviteye database instance
    Pdb.populate_db()

    # Initialization SMS message
    logger.log_it('Starting Program...')
    tw.send_message('Piviteye Program Initalized.')
    start_time = datetime.datetime.now()

    # Setup the GPIO using pin 14 & 15 and default to True
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, True)
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, True)

    # Call Main()
    main()
