from RPi import GPIO
from utility.pizypwm import *
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
        GPIO.setwarnings(False)
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

    def pwm_mode(self):
        self._mode = 4

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
                sleep(1)
            elif self._mode == 3:
                self._led_on()
                sleep(0.25)
                self._led_off()
                sleep(0.25)
            elif self._mode == 4:
                led_pwm = PiZyPwm(100, self._gpio, GPIO.BCM)
                led_pwm.start(100)
                dim_up = range(0, 80)
                dim_down = range(80, 0)
                while self._mode == 4:
                    for power in dim_up:
                        led_pwm.changeDutyCycle(power)
                        sleep(0.01)
                        if self._mode != 4:
                            break
                    for power in dim_down:
                        led_pwm.changeDutyCycle(power)
                        sleep(0.01)
                        if self._mode != 4:
                            break


class LedAssembly(Observer, LoggerSuper):
    """
    Сборка светодоиодов с логикой работы
    """
    logger = logging.getLogger('LedAssembly')
    def __init__(self, model):
        self.model = model
        self.red_led = LED(gpio=2, name='red')
        self.green_led = LED(gpio=3, name='green')

    def model_is_changed(self):
        if self.model.permission:
            self.green_led.blink_fast()
        else:
            self.green_led.led_off()

        if self.model.connected:
            self.red_led.pwm_mode()
        else:
            self.red_led.blink()