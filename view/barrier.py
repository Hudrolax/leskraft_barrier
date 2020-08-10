from utility.observer import Observer
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from time import sleep
import logging
import threading


class Barrier(Observer, LoggerSuper, BaseClass):
    """
    Класс описывает управление шлагбаумом
    """
    logger = logging.getLogger('Barrier')

    def __init__(self, model):
        self.model = model
        self._open = False
        self._watchdog_thread = threading.Thread(target=self._threaded_func, args=(), daemon=True)
        self._watchdog_thread.start()

    def open(self):
        self.logger.info('открыл шлагбаум')

    def close(self):
        self.logger.info('закрыл шлагбаум')

    def _threaded_func(self):
        while self.working():
            if self._open:
                self.open()
                sleep(5)
                self.close()
                self.model.reset_permission()
                self._open = False
            sleep(0.1)


    def model_is_changed(self):
        if self.model.permission:
            self._open = True