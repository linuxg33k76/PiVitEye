# Alarm Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date: August 21, 2016 v1.0.0
# Revision:

# This program sends sounds an alarm

# Import class files

import pygame
import os


def main():

    # Get Relative Path info, and append sound file from ./SupportFiles/ directory
    file_path = os.path.dirname(__file__)
    support_files_dir = 'SupportFiles/'
    path = os.path.join(file_path, support_files_dir, 'bank_alarm_3.wav')

    # Sound Alarm
    pygame.mixer.init()

    # Set volume to max
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load(path)

    # Play wave file 6x (0 or none is once, 1 is two times, 2 is three times, etc.)
    pygame.mixer.music.play(5)

    while pygame.mixer.music.get_busy() is True:
        continue

if __name__ == "__main__":
    main()
