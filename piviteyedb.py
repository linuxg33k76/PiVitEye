#!/usr/bin/env python3

#Piviteye Database Class
#Author:  Ben Calvert
#Date:  October 11, 2016 v1.0.0
#Revision:  February 25, 2017 v1.1.0 - added status pi command to display uptime

#This Class handles all DB functions

#Import class files
import sqlite3

class PyVitEyeDB(object):
    directory = '/opt/piviteye'
    database = directory + '/SupportFiles/piviteye.db'

    def __init__(self):

        '''
        Create Database called piviteye.db, create a table called COMMANDS
        with the following data format:
        Primary Key - ID
        CMD - text command string
        LOGMSG - text log message
        SMSTXT - text SMS message
        PICMD - text pi command
        SUBCALL - text sub process call string
        '''
        # Create the database
        conn = sqlite3.connect(self.database)

        # Drop table to clear out old data

        conn.execute('''DROP TABLE IF EXISTS COMMANDS;''')

        # Create new table COMMANDS
        conn.execute('''CREATE TABLE COMMANDS
                     (ID INT PRIMARY KEY NOT NULL,
                     CMD TEXT NOT NULL,
                     LOGMSG TEXT NOT NULL,
                     SMSMSG TEXT NOT NULL,
                     PICMD TEXT,
                     SUBCALL TEXT);''')

        # Add Data to Table COMMANDS
        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (1,'list','Sending the Available Commands List.','Executed - list command. Valid Commands: close, open, restart, webcam, picam, video, halt, shutdown, disarm, arm, mute, unmute, volmax, volmin, volmid, voltest, status, uptime, update, tshark and list.','','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (2, 'close','Closing Garage Door','Executed - close command.','garage_door','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (3, 'open','Opening Garage Door','Executed - open command.','garage_door','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (4, 'webcam','Taking a Picture with Webcam...','Executed - webcam command.','','SupportFiles/webcam.sh');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (5,'restart','Restarting System Program...','Executing - restart command...','','sudo shutdown -r now');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (6,'picam','Taking a Picture with Pi Camera...','Executed - picam command.','picam','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (7,'video','Taking a Video with Pi Camera...','Executed - 60 second video command.','pivideo','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (8,'shutdown','User Initiated Shutting Down of the System.','Executing - shutdown command.','','sudo shutdown -h now');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (9,'disarm','User Initiated Stop of motion service.','Executing - stopping motion service.','','sudo service motion stop');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (10,'arm','User Initiated Start of motion service.','Executing - starting motion service.','','sudo service motion start');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (11,'mute','User Initiated Alarm Sound Mute.','Executing - Muting Alarm.','','sudo amixer set PCM mute');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (12,'unmute','User Initiated Alarm Sound Unmute.','Executing - Unmuting Alarm.','','sudo amixer set PCM unmute');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (13,'volmax','User Initiated Volume Max.','Executing - Volume to 100%.','','sudo amixer set PCM 100%');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (14,'volmin','User Initiated Volume Min.','Executing - Volume to 0%.','','sudo amixer set PCM 0%');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (15,'volmid','User Initiated Volume Mid.','Executing - Volume to 80%.','','sudo amixer set PCM 80%');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (16,'voltest','User Initiated Alarm Test.','Executing - Alarm Test.','','sh SupportFiles/play_sound.sh');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (17,'halt','User Initiated Stop of Program Execution.','Executing - program shutdown.','halt','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (18,'status','User Requested System Status.','I am ALIVE!','status','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (19,'uptime','User Requested System Uptime.','Getting System Uptime.','uptime','');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (20,'update','User Requested System Update.','Updating Raspberry Pi 3...','','sudo apt-get update && sudo apt-get upgrade -y');''')

        conn.execute('''INSERT INTO COMMANDS (ID,CMD,LOGMSG,SMSMSG,PICMD,SUBCALL) \
                     VALUES (21,'tshark','User Requested Packet Capture on eth0.','Capturing Network Traffic on eth0 FOR 1 minute...','','sh SupportFiles/tshark.sh');''')

        # Commit Data
        conn.commit()


    def get_all_commands(self):

        '''
        Returns all rows of commands from the database.
        '''

        conn = sqlite3.connect(self.database)
        rows = conn.execute("SELECT * FROM COMMANDS")
        return rows

    def get_command(self,command):

        '''
        Returns an array of results for the given command.
        '''

        self.command = command
        conn = sqlite3.connect(self.database)
        row = conn.execute(("SELECT * FROM commands WHERE cmd = \'{0}\' ;").format(self.command))
        result = []
        for item in row:
            for elem in item:
                result.append(elem)
        return result
