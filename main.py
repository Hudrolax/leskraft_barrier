from controller.barcode_scanner import BarScanner
from controller.keyboard_input import Keyboard
from model.http_getter import HttpGetter
from model.data_base import DB
from view.barrier import Barrier
from time import sleep
import os
from dotenv import load_dotenv
import logging

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.WARNING
LOG_LEVEL = logging.INFO

if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

    bar_scanner_com_port = os.getenv("BAR_SCANNER_COM_PORT")
    opengate_server = os.getenv("OPENGATE_SERVER")
    opengate_port = os.getenv("OPENGATE_PORT")
    open_codes_route = os.getenv("OPEN_CODES_ROUTE")
    send_open_event_route = os.getenv("SEND_OPEN_EVENTS_ROUTE")
    opengate_user = os.getenv("OPENGATE_USER")
    opengate_password = os.getenv("OPENGATE_PASS")

    print('hello')
    data_base = DB()
    http_getter = HttpGetter(data_base, opengate_server, opengate_port, open_codes_route, send_open_event_route, opengate_user, opengate_password)
    scanner = BarScanner(bar_scanner_com_port, http_getter)
    barrier = Barrier(http_getter)
    http_getter.add_observer(barrier)

    keyboard_input = Keyboard(data_base)
    while True:
        # main loop
        sleep(1)