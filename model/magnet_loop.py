from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from RPi import GPIO
from time import sleep
import logging
import threading
from datetime import datetime


class Magnet_loop(LoggerSuper):
    logger = logging.getLogger('Magnet_loop_view')

    def __init__(self):
        self._input_pin = 17
        self._ouput_pin = 25
        self._loop_state = False
        self._last_loop_output_signal = datetime.now()
        self._loop_true_signal_timer = 0
        GPIO.setwarnings(False)
        GPIO.setup(self._input_pin, GPIO.IN)
        GPIO.setup(self._ouput_pin, GPIO.OUT)
        GPIO.output(self._ouput_pin, True)
        self._input_thread = threading.Thread(target=self._threaded_read_input_pin, args=(), daemon=True)
        self._input_thread.start()
        self._output_thread = threading.Thread(target=self._threaded_output_loop, args=(), daemon=True)
        self._output_thread.start()

    def get_loop_state(self):
        return self._loop_state

    def get_last_loop_output_signal(self):
        return self._last_loop_output_signal

    def _threaded_read_input_pin(self):
        """"
        Функция в потоке проверяет сигнал с магнитной петли
        Сработка магнитной петли считается моментально после получения HIGH
        Окончание сработки считается через _N повторений цикла с учетом паузы 0.1 сек
        """
        _N = 20
        while BaseClass.working():
            if GPIO.input(self._input_pin) == GPIO.HIGH:
                self._loop_true_signal_timer = _N # цикл срабатывает раз в 0.1с, значит через _N отсчетов пройдет _N/10 сек
                self._loop_state = True
                self._last_loop_output_signal = datetime.now()
            else:
                if self._loop_true_signal_timer > 0:
                    self._loop_true_signal_timer -= 1
                if self._loop_true_signal_timer == 0:
                    self._loop_state = False
            sleep(0.1)

    def _threaded_output_loop(self):
        while BaseClass.working():
            if self._loop_state:
                GPIO.output(self._ouput_pin, False)
            else:
                GPIO.output(self._ouput_pin, True)
            sleep(0.1)
