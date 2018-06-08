
# Piviteye Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date:  May 27, 2016 v1.0.0
# Revision:  May 30, 2018 v1.2.1

# This program takes SMS messages and initiates actions based on command Rx'd

# Import class files

from gpiozero import LED, Button
from time import sleep
import subprocess
import datetime
import json
from Classes import twclass
from Classes import piviteyedb as Pdb
from Classes import picamclass
from Classes import programlogclass

# Define Pi Command


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


def toggle_relay():
    # # GPIO Object Instances
    relay = LED(17)
    relay.off()
    sleep(3)
    relay.on()

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
            msg = messages[0].body.lower().strip()

            # store last message's sid number (ID number)
            msg_num = messages[0].sid
            logger.log_it('New Rx Message ID -> ' + msg_num)
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
                tw.send_message(command.smsmsg)
                if command.picmd != '':
                    pi_command(command.picmd)

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
    # Call Main()
    main()
