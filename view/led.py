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
        self._gpio = gpio
        GPIO.setwarnings(False)
        GPIO.setup(self._gpio, GPIO.OUT)  # Настраиваем GPIO пин на вывод

    def led_on(self):
        GPIO.output(self._gpio, True)

    def led_off(self):
        GPIO.output(self._gpio, False)


class LedAssembly:
    """
    Сборка светодоиодов с логикой работы
    self._mode =
    0 - all OFF (lost connection)
    1 - red blink, green off (exist connection)
    2 - green blink fast, red off (access to opening)
    3 - red blink fast, green off (deny to opening)
    """
    def __init__(self, model):
        self.model = model # HTTP service
        self._mode = 0
        self.red_led = LED(gpio=2, name='red')
        self.green_led = LED(gpio=3, name='green')
        self._led_thread = threading.Thread(target=self._led_threaded_func, args=(), daemon=False)
        self._led_thread.start()
        self._condition_thread = threading.Thread(target=self._condition_thread_func, args=(), daemon=False)
        self._condition_thread.start()

    def _condition_thread_func(self):
        while BaseClass.working():
            self._mode = 0
            if self.model.connected:
                self._mode = 1
            if self.model.bool_get_permission:
                if self.model.permission:
                    self._mode = 2
                else:
                    self._mode = 3
            sleep(0.1)

    def _sleep(self, ms, mode):
        for k in range(0, ms):
            sleep(0.001)
            if self._mode != mode:
                return

    def _led_threaded_func(self):
        while BaseClass.working():
            self._mode = 0
            if self.model.connected:
                self._mode = 1
            if self.model.bool_get_permission:
                if self.model.permission:
                    self._mode = 2
                else:
                    self._mode = 3

            if self._mode == 0:
                self.green_led.led_off()
                self.red_led.led_off()
                sleep(0.1)
            elif self._mode == 1:
                self.green_led.led_off()
                self.red_led.led_on()
                self._sleep(1000, 1)
                self.red_led.led_off()
                self._sleep(1000, 1)
            elif self._mode == 2:
                self.red_led.led_off()
                for k in range (0, 30):
                    self.green_led.led_on()
                    sleep(0.125)
                    self.green_led.led_off()
                    sleep(0.125)
                self.model.bool_get_permission = False
            elif self._mode == 3:
                self.green_led.led_off()
                for k in range(0, 15):
                    self.red_led.led_on()
                    sleep(0.125)
                    self.red_led.led_off()
                    sleep(0.125)
                self.model.bool_get_permission = False
        self.green_led.led_off()
        self.red_led.led_off()