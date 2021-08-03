
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
from Classes import piviteyedb as PDB
from Classes import picamclass
from Classes import programlogclass
from Classes import openweatherclass as OWC


# Get Weather function

def get_weather(zipcode):
    # Get weather info for Zipcode from OpenWeatherAPI
    with open('/etc/piviteye/openweather.conf') as apikeyfile:
        apikey = json.load(apikeyfile)['openweatherapikey']
        # apikey = key['openweatherapikey']
    w = OWC.OpenWeatherAPI(apikey, zipcode)
    results = w.get_weather_data()
    return results


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
    elif command == 'weather_info':
        # Get weather by calling weather class
        message = get_weather(vars)
        tw.send_message(message)
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

            # Store message parts as an array; separate by "whitespace"
            msg_array = messages[0].body.lower().split(" ")

            # Store parts of message for use in command execution
            msg = msg_array[0]
            if len(msg_array) == 2:
                msg_vars = msg_array[1]
            else:
                msg_vars = '' 

            # store last message's sid number (ID number)
            msg_num = messages[0].sid
            logger.log_it('Rx Message ID -> ' + msg_num)

        except(e):
            logger.log_it('Unable to process message.')

        # check message status and pull recieved messages only
        if messages[0].status == 'received' and msg_num != old_msg_id:

            # log message in logfile
            logger.log_it('Command was --> ' + msg)

            # look up command in database (piviteye.db)
            
            command = PDB.get_command(msg)
            
            # Check for valid commands
            if command is not None:
                logger.log_it(command.logmsg)

                # Execute command
                if command.picmd != '':
                    pi_command(command.picmd, msg_vars)

                # Send Message on command; check for variable in relay commands
                if msg_vars !='' and 'relay' in msg:
                    tw.send_message((command.smsmsg + ' with variable {0} seconds').format(msg_vars))
                elif msg_vars !='' and 'weather' in msg:
                    tw.send_message((command.smsmsg + ' with variable {0}').format(msg_vars))
                else:
                    tw.send_message(command.smsmsg)
                
                # Linux Subsystem Calls
                if command.subcall != "":
                    cmd_response = subprocess.call(command.subcall, shell=True)
                    if cmd_response == 0:
                        tw.send_message('Command Completed Successfully!')
                    else:
                        tw.send_message(('Command failed with code: {0}... :(').format(str(cmd_response)))

            else:

                # Failure option for bad commands (commands not in Database)
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
    PDB.populate_db()

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
