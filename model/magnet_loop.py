from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from RPi import GPIO
from time import sleep
import logging
import threading


class Magnet_loop(LoggerSuper):
    logger = logging.getLogger('Magnet_loop_view')

    def __init__(self):
        self._input_pin = 17
        self._ouput_pin = 25
        self._loop_state = False
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ouput_pin, GPIO.IN)
        GPIO.setup(self._ouput_pin, GPIO.OUT)
        GPIO.output(self._ouput_pin, True)
        self._input_thread = threading.Thread(target=self._threaded_read_input_pin, args=(), daemon=True)
        self._input_thread.start()
        self._output_thread = threading.Thread(target=self._threaded_output_loop, args=(), daemon=True)
        self._output_thread.start()

    def _threaded_read_input_pin(self):
        while BaseClass.working():
            if GPIO.input(self._input_pin) == GPIO.HIGH:
                self._loop_state = True
            else:
                self._loop_state = False
            sleep(0.1)
            self._loop_state = True
            sleep(10)
            self._loop_state = False

    def _threaded_output_loop(self):
        while BaseClass.working():
            if self._loop_state:
                GPIO.output(self._ouput_pin, False)
            else:
                sleep(3)
                GPIO.output(self._ouput_pin, True)
            sleep(0.1)
