from view.led import LedAssembly
from time import sleep

if __name__ == '__main__':
    led = LedAssembly(None)
    led.green_led.led_on()
    sleep(0.5)
    led.green_led.led_off()
    sleep(0.5)
    led.green_led.led_on()
    sleep(0.5)
    led.green_led.led_off()
    led.green_led.blink_fast()