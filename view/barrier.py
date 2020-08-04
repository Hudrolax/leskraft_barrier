from utility.observer import Observer
from utility.logger_super import LoggerSuper
from time import sleep
import logging


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