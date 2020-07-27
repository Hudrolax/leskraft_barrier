from controller.barcode_scanner import BarScanner
from controller.keyboard_input import Keyboard
from model.http_getter import HttpGetter
from model.data_base import DB
from view.arduino_barrier import ArduinoBarrier as Barrier
from time import sleep
import logging

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.WARNING
LOG_LEVEL = logging.INFO

bar_scanner_com_port = 'COM3'
opengate_server = 'golden1'
opengate_port = '80'
opengate_route = '/trade2016donate/hs/barrier/get_perrmission'
admin_codes_route = '/trade2016donate/hs/barrier/get_admin_codes'
opengate_user = 'http_services'
opengate_password = 'lk93295841lk'

if __name__ == '__main__':
    print('hello')
    data_base = DB()
    http_getter = HttpGetter(data_base, opengate_server, opengate_port, opengate_route, admin_codes_route, opengate_user, opengate_password)
    scanner = BarScanner(bar_scanner_com_port, http_getter)
    barrier = Barrier(http_getter)
    http_getter.add_observer(barrier)

    keyboard_input = Keyboard(data_base)
    while True:
        # main loop
        sleep(1)