from RPi import GPIO
from utility.observer import Observer
from utility.base_class import BaseClass
import threading
import logging
from time import sleep


class LED:
    """
    Класс LED отвечает за объект светодиода. Обеспечивает методы его сигналов.
    """
    def __init__(self, gpio, name:str = None):
        self._name = name
        self._mode = 0 # 0 - OFF, 1 - ON, 2 - blink, 3 - blink fast
        self._gpio = gpio
        GPIO.setwarnings(False)
        GPIO.setup(self._gpio, GPIO.OUT)  # Настраиваем GPIO пин на вывод
        self._thread = threading.Thread(target=self._led_threaded_func, args=(), daemon=False)
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

    def _sleep(self, ms, mode):
        for k in range(0, ms):
            sleep(0.001)
            if self._mode != mode:
                return

    def _led_threaded_func(self):
        while BaseClass.working():
            if self._mode == 0:
                self._led_off()
            elif self._mode == 1:
                self._led_on()
            elif self._mode == 2:
                self._led_on()
                self._sleep(1000, 2)
                self._led_off()
                self._sleep(1000, 2)
            elif self._mode == 3:
                for k in range(0, 24):
                    self._led_on()
                    self._sleep(125, 3)
                    self._led_off()
                    self._sleep(125, 3)
            sleep(0.1)
        self._led_off()


class LedAssembly(Observer):
    """
    Сборка светодоиодов с логикой работы
    """
    def __init__(self, model):
        self.model = model
        self.red_led = LED(gpio=2, name='red')
        self.green_led = LED(gpio=3, name='green')

    def model_is_changed(self):
        if self.model.connected:
            if self.model.bool_get_permission:
                if self.model.permission:
                    self.red_led.led_off()
                    self.green_led.blink_fast()
                else:
                      self.green_led.led_off()
                    self.red_led.blink_fast()
            else:
                self.red_led.blink()
                self.green_led.led_off()
        else:
            self.green_led.blink()
            self.red_led.blink()