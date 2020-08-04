from utility.observer import Observer
from utility.logger_super import LoggerSuper
from time import sleep

import logging

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING

if WRITE_LOG_TO_FILE:
    logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')
else:
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

class Barrier(Observer, LoggerSuper):
    """
    Класс описывает управление шлагбаумом
    """
    logger = logging.getLogger('Barrier')

    def __init__(self, model):
        self.model = model

    def open(self):
        self.logger.debug('открыл шлагбаум')

    def close(self):
        self.logger.debug('закрыл шлагбаум')

    def modelIsChanged(self):
        self.open()
        sleep(5)
        self.close()