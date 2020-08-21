from RPi import GPIO
from utility.observer import Observer
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from time import sleep
import logging
import threading


class Barrier(Observer, LoggerSuper):
    """
    Класс описывает управление шлагбаумом
    """
    logger = logging.getLogger('Barrier')

    def __init__(self, model):
        self._open_pin = 23
        self._close_pin = 23
        self.model = model
        self._open = False
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # говорим о том, что мы будем обращаться к контактам по номеру канала
        GPIO.setup(self._open_pin, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        GPIO.setup(self._close_pin, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        GPIO.output(self._open_pin, True)
        GPIO.output(self._close_pin, True)
        self._barrier_thread = threading.Thread(target=self._threaded_func, args=(), daemon=True)
        self._barrier_thread.start()

    def open(self):
        GPIO.output(self._open_pin, False)
        sleep(1)
        GPIO.output(self._open_pin, True)
        self.logger.info('открыл шлагбаум')

    def close(self):
        GPIO.output(self._close_pin, False)
        sleep(1)
        GPIO.output(self._close_pin, True)
        self.logger.info('закрыл шлагбаум')

    def _threaded_func(self):
        while BaseClass.working():
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