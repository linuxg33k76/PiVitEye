# programlogclass
# Created by Ben Calvert on 10/13/16.

import datetime
import logging


class ProgramLog (object):
    '''
    Program Logger Class
    '''

    def __init__(self):
        self.time = datetime.datetime.now().strftime("%A-%d-%B-%Y-%I:%M%p")
        self.path = '/mnt/usb/log/'
        filename = self.path + 'piviteye.log'
        self.logger = logging.getLogger('Pi_vit_eye app')
        self.hdlr = logging.FileHandler(filename)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def log_it(self, message):
        logger = self.logger
        logger.info(message)

    def log_warn(self, message):
        logger = self.logger
        logger.warning(message)
