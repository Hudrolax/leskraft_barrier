from RPi import GPIO
from utility.logger_super import LoggerSuper
from utility.observer import Observer
import threading
import logging
from time import sleep


class LED:
    """
    Класс LED отвечает за объект светодиода. Обеспечивает методы включения и отключения светодиода.
    """
    def __init__(self, gpio, name:str = None):
        self._name = name
        self._mode = 0 # 0 - OFF, 1 - ON, 2 - blink, 3 - blink fast
        self._gpio = gpio
        GPIO.setmode(GPIO.BCM)  # говорим о том, что мы будем обращаться к контактам по номеру канала
        GPIO.setup(self._gpio, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        self._thread = threading.Thread(target=self._led_threaded_func, args=(), daemon=True)
        self._thread.start()


    def led_on(self):
        self._mode = 1

    def led_off(self):
        self._mode = 0

    def blink(self):
        self._mode = 2

    def blink_fast(self):
        self._mode = 3

    def _led_on(self):
        GPIO.output(self._gpio, True)

    def _led_off(self):
        GPIO.output(self._gpio, False)

    def _led_threaded_func(self):
        while True:
            if self._mode == 0:
                self._led_off()
            elif self._mode == 1:
                self._led_on()
            elif self._mode == 2:
                self._led_on()
                sleep(1)
                self._led_off()
            elif self._mode == 3:
                self._led_on()
                logging.warning('blink_on')
                sleep(1)
                logging.warning('blink_off')
                self._led_off()


class LedAssembly(Observer, LoggerSuper):
    """
    Сборка светодоиодов с логикой работы
    """
    logger = logging.getLogger('LedAssembly')
    def __init__(self, model):
        self.model = model
        self.red_led = LED(gpio=23, name='red')
        self.green_led = LED(gpio=24, name='green')

    def model_is_changed(self):
        if self.model.permission:
            self.green_led.blink_fast()
        else:
            self.green_led.led_off()

        if self.model.connected:
            self.red_led.led_on()
        else:
            self.red_led.blink()