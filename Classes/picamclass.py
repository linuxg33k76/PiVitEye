# picamclass
# Created by Ben Calvert on 10/13/16.

import datetime
import subprocess
from picamera import PiCamera
from Classes import programlogclass as logger


class PiCam(object):

    def __init__(self):

        '''
        Initialize the class with file and timestamp data
        '''

        self.time = datetime.datetime.now().strftime("%A-%d-%B-%Y-%I_%M%p")
        self.path = '/mnt/usb/video/'

    # Picture Method - takes snapshot and creates a file with date/time timestamp

    def take_picture(self, rotation):
        filename = self.path + self.time + '.jpg'
        logger.log_it(filename)
        camera = PiCamera()
        camera.rotation = rotation
        camera.annotate_text = self.time
        sleep(5)
        camera.capture(filename)
        sleep(5)

    # Video Method - takes 60sec of video and creates a file with date/time timestamp

    def take_video(self, rotation):

        # Save the video to a temporary location /tmp

        path = '/tmp/'
        temp_filename = path + self.time + '.h264'
        video = PiCamera()
        video.rotation = rotation
        video.annotate_text = self.time
        video.start_recording(temp_filename)
        sleep(60)
        video.stop_recording()

        # Convert video to something viewable (MP4)
        filename = self.path + self.time + '.mp4'
        conv_command = 'MP4Box -add {0} {1}'.format(temp_filename, filename)
        print(conv_command)
        logger.log_it(filename)
        subprocess.call(conv_command, shell=True)
        sleep(15)
