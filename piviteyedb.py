# !/usr/bin/env python3

# Piviteye Database Class
# Author:  Ben Calvert
# Date:  October 11, 2016 v1.0.0
# Revision:  February 25, 2017 v1.1.0 - added status pi command to display uptime
# Revision:  May 2107 v.1.3.0 - removed SQLite3 and added Pony ORM

# This Class handles all DB functions

# Import class files
# import sqlite3
from pony.orm import *

# Instantiate a new db Object
db = Database()

# Set up database connection - store db in memory
db.bind('sqlite', ':memory:', create_db=True)


# Declare data Models as classes
class Commands(db.Entity):
    # _table_ = "COMMANDS"
    id = PrimaryKey(int, auto=True)
    cmd = Required(str)
    logmsg = Required(str)
    smsmsg = Required(str)
    picmd = Optional(str)
    subcall = Optional(str)


# sql_debug(True)
# Map models to database, but DO NOT create the tables
db.generate_mapping(create_tables=True)


# Set Commands
@db_session
def populate_db():
    c1 = Commands(id=1,
                  cmd='list',
                  logmsg='Sending the Available Commands List.',
                  smsmsg='Executed - list command. Valid Commands: close, open, restart, record, picam, pivideo, halt, shutdown, disarm, arm, mute, unmute, volmax, volmin, volmid, voltest, status, uptime, update, tshark and list.',
                  picmd='',
                  subcall='')

    c2 = Commands(id=2,
                  cmd='close',
                  logmsg='Closing Garage Door',
                  smsmsg='Executed - close command.',
                  picmd='garage_door',
                  subcall='')

    c3 = Commands(id=3,
                  cmd='open',
                  logmsg='Opening Garage Door',
                  smsmsg='Executed - open command.',
                  picmd='garage_door',
                  subcall='')

    c4 = Commands(id=4,
                  cmd='record',
                  logmsg='Taking a 60 second Video with Webcam...',
                  smsmsg='Executed - webcam command.',
                  picmd='',
                  subcall='SupportFiles/webcam.sh')
    c5 = Commands(id=5,
                  cmd='restart',
                  logmsg='Restarting System Program...',
                  smsmsg='Executing - restart command...',
                  picmd='',
                  subcall='sudo shutdown -r now')
    c6 = Commands(id=6,
                  cmd='picam',
                  logmsg='Taking a Picture with Pi Camera...',
                  smsmsg='Executed - picam command.',
                  picmd='picam',
                  subcall='')
    c7 = Commands(id=7,
                  cmd='pivideo',
                  logmsg='Taking a Video with Pi Camera...',
                  smsmsg='Executed - 60 second video command.',
                  picmd='pivideo',
                  subcall='')
    c8 = Commands(id=8,
                  cmd='shutdown',
                  logmsg='User Initiated Shutting Down of the System.',
                  smsmsg='Executing - shutdown command.',
                  picmd='',
                  subcall='sudo shutdown -h now')
    c9 = Commands(id=9,
                  cmd='disarm',
                  logmsg='User Initiated Stop of motion service.',
                  smsmsg='Executing - stopping motion service.',
                  picmd='',
                  subcall='sudo service motion stop')
    c10 = Commands(id=10,
                   cmd='arm',
                   logmsg='User Initiated Start of motion service.',
                   smsmsg='Executing - starting motion service.',
                   picmd='',
                   subcall='sudo service motion start')
    c11 = Commands(id=11,
                   cmd='mute',
                   logmsg='User Initiated Alarm Sound Mute.',
                   smsmsg='Executing - Muting Alarm.',
                   picmd='',
                   subcall='sudo amixer set PCM mute')
    c12 = Commands(id=12,
                   cmd='unmute',
                   logmsg='User Initiated Alarm Sound Unmute.',
                   smsmsg='Executing - Unmuting Alarm.',
                   picmd='',
                   subcall='sudo amixer set PCM unmute')
    c13 = Commands(id=13,
                   cmd='volmax',
                   logmsg='User Initiated Volume Max.',
                   smsmsg='Executing - Volume to 100%.',
                   picmd='',
                   subcall='sudo amixer set PCM 100%')
    c14 = Commands(id=14,
                   cmd='volmin',
                   logmsg='User Initiated Volume Min.',
                   smsmsg='Executing - Volume to 0%.',
                   picmd='',
                   subcall='sudo amixer set PCM 0%')
    c15 = Commands(id=15,
                   cmd='volmid',
                   logmsg='User Initiated Volume Mid.',
                   smsmsg='Executing - Volume to 80%.',
                   picmd='',
                   subcall='sudo amixer set PCM 80%')
    c16 = Commands(id=16,
                   cmd='voltest',
                   logmsg='User Initiated Alarm Test.',
                   smsmsg='Executing - Alarm Test.',
                   picmd='',
                   subcall='sh SupportFiles/play_sound.sh')
    c17 = Commands(id=17,
                   cmd='halt',
                   logmsg='User Initiated Stop of Program Execution.',
                   smsmsg='Executing - program shutdown.',
                   picmd='halt',
                   subcall='')
    c18 = Commands(id=18,
                   cmd='status',
                   logmsg='User Requested System Status.',
                   smsmsg='I am ALIVE!',
                   picmd='status',
                   subcall='')
    c19 = Commands(id=19,
                   cmd='uptime',
                   logmsg='User Requested System Uptime.',
                   smsmsg='Getting System Uptime.',
                   picmd='uptime',
                   subcall='')
    c20 = Commands(id=20,
                   cmd='update',
                   logmsg='User Requested System Update.',
                   smsmsg='Updating Raspberry Pi 3...',
                   picmd='',
                   subcall='sudo apt-get update && sudo apt-get upgrade -y')
    c21 = Commands(id=21,
                   cmd='tshark',
                   logmsg='User Requested Packet Capture on eth0.',
                   smsmsg='Capturing Network Traffic on eth0 FOR 1 minute...',
                   picmd='',
                   subcall='sh SupportFiles/tshark.sh')

    commit()


# Format results as Dictionary - For Testing Purposes
def format_results(data):
    # create a dictionary object of each result
    results = []
    if data is not None:
        for row in data:
            results.append(row.to_dict())
    print(results)


# Get Counters
@db_session
def get_count(model):
    result = model.select().count()
    return result


# Get Systems query
@db_session
def get_commands():
    # Get a list of objects (hint; use the [:] slice operator)
    results = Commands.select()[:]
    format_results(results)
    return results


# Get System query
@db_session
def get_command(name):
    # Get a system by ivue_name
    results = Commands.get(cmd=name)
    # format_results(results)
    return results
