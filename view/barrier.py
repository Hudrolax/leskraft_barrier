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
        self._openned = False

    def open(self):
        self.logger.info('открыл шлагбаум')

    def close(self):
        self.logger.info('закрыл шлагбаум')

    def model_is_changed(self):
        if not self._openned and self.model.permission:
            self._openned = True
            self.open()
            sleep(5)
            self.close()
            self._openned = False