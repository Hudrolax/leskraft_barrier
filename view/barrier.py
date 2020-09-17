from RPi import GPIO
from utility.observer import Observer
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from time import sleep
import logging
import threading
from model.magnet_loop import Magnet_loop
from datetime import datetime


class Barrier(Observer, LoggerSuper):
    """
    Класс описывает управление шлагбаумом
    """
    logger = logging.getLogger('Barrier')

    def __init__(self, model):
        self._CLOSE_BY_MAGNET_LOOP_DELAY = 5
        self._CLOSE_BY_TIMER_DELAY = 120
        self._CLOSE_BY_TIMER_DELAY_FORCIBLY = 0

        self._close_by_magnet_loop = True # закрывать по магнитной петле
        self._open_pin = 23
        self._close_pin = 24
        self.model = model
        self._magnet_loop = Magnet_loop()
        self._to_open = False
        self._openned = False
        self._closed_by_timer_forcibly_timer = datetime.now()
        GPIO.setwarnings(False)
        GPIO.setup(self._open_pin, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        GPIO.setup(self._close_pin, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        GPIO.output(self._open_pin, True)
        GPIO.output(self._close_pin, True)
        self._last_opening_time = datetime.now()
        self._barrier_thread = threading.Thread(target=self._threaded_func, args=(), daemon=True)
        self._barrier_thread.start()

    def get_closing_by_magnet_loop(self):
        if self._close_by_magnet_loop:
            return 'yes'
        else:
            return 'no'

    def get_magnet_loop_delay(self):
        return self._CLOSE_BY_MAGNET_LOOP_DELAY

    def get_timer_delay(self):
        return self._CLOSE_BY_TIMER_DELAY

    def get_timer_delay_forcibly(self):
        return self._CLOSE_BY_TIMER_DELAY_FORCIBLY

    def set_close_by_magnet_loop(self, val):
        if isinstance(val, bool):
            self._close_by_magnet_loop = val
        else:
            self.logger.error(f'set_close_by_magnet_loop type error!!!. Type val is {type(val)}. Need bool.')

    def open(self):
        self._last_opening_time = datetime.now()
        self._openned = True
        GPIO.output(self._open_pin, False)
        sleep(1)
        GPIO.output(self._open_pin, True)
        self.logger.info('открыл шлагбаум')

    def close(self):
        GPIO.output(self._close_pin, False)
        sleep(1)
        GPIO.output(self._close_pin, True)
        self._openned = False
        self.logger.info('закрыл шлагбаум')

    def _threaded_func(self):
        while BaseClass.working():
            # opening algorithm
            if self._to_open:
                self.open()
                self._magnet_loop.wait_for_signal = True
                self._to_open = False
                self.model.reset_permission()
            else:
                if (datetime.now() - self._last_opening_time).total_seconds() < 5:
                    sleep(0.5)
                    continue
                # closing by magnet loop
                if self._close_by_magnet_loop and self._openned and not self._magnet_loop.wait_for_signal\
                        and (datetime.now() - self._magnet_loop.get_last_loop_output_signal()).total_seconds() > self._CLOSE_BY_MAGNET_LOOP_DELAY:
                    self.close()
                    self.logger.info(f'Закрыл шлагбаум по магнитной петле. Задержка после проезда {self._CLOSE_BY_MAGNET_LOOP_DELAY} сек.')

                # closing by timer
                if self._CLOSE_BY_TIMER_DELAY > 0 and self._openned and (datetime.now() - self._last_opening_time).total_seconds() > self._CLOSE_BY_TIMER_DELAY:
                    self.close()
                    self.logger.info(f'Закрыл шлагбаум по таймеру. Задержка после открытия {self._CLOSE_BY_TIMER_DELAY} сек.')

                # closing by timer forcibly
                if 7 < datetime.now().hour < 19 and 0 < self._CLOSE_BY_TIMER_DELAY_FORCIBLY < (
                        datetime.now() - self._closed_by_timer_forcibly_timer).total_seconds() and\
                        (datetime.now() - self._last_opening_time).total_seconds() > self._CLOSE_BY_TIMER_DELAY + self._CLOSE_BY_TIMER_DELAY_FORCIBLY:
                    self._closed_by_timer_forcibly_timer = datetime.now()
                    self.close()
                    self.logger.info(
                        f'Закрыл шлагбаум по таймеру принудительно. Период закрытия каждые {self._CLOSE_BY_TIMER_DELAY_FORCIBLY} сек.')

            sleep(0.1)


    def model_is_changed(self):
        self._close_by_magnet_loop = self.model.get_closing_by_magnet_loop()
        self._CLOSE_BY_TIMER_DELAY = self.model.get_closing_by_timer()
        self._CLOSE_BY_TIMER_DELAY_FORCIBLY = self.model.get_closing_by_timer_forcibly()

        if self.model.permission:
            self._to_open = True