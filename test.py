from view.led import LedAssembly
from time import sleep
from RPi import GPIO

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)  # говорим о том, что мы будем обращаться к контактам по номеру канала
    GPIO.setup(3, GPIO.OUT)  # Настраиваем GPIO пин на вывод
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)
    GPIO.output(3, True)
    sleep(0.25)
    GPIO.output(3, False)
    sleep(0.25)