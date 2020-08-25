from controller.barcode_scanner import BarScanner
from controller.keyboard_input import Keyboard
from model.http_getter import HttpGetter
from model.data_base import DB
from view.barrier import Barrier
from view.led import LedAssembly
from utility.class_watchdog import WatchDog
from utility.base_class import BaseClass
from time import sleep
import os
from dotenv import load_dotenv
import logging
from RPi import GPIO


if __name__ == '__main__':
    WRITE_LOG_TO_FILE = False
    LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
    LOG_LEVEL = logging.INFO
    logger = logging.getLogger('main')

    if WRITE_LOG_TO_FILE:
        logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL,
                            datefmt='%d/%m/%y %H:%M:%S')
    else:
        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

    watchdog_com_port = os.getenv("WATCHDOG_COM_PORT")
    bar_scanner_com_port = os.getenv("BAR_SCANNER_COM_PORT")
    opengate_server = os.getenv("OPENGATE_SERVER")
    opengate_port = os.getenv("OPENGATE_PORT")
    open_codes_route = os.getenv("OPEN_CODES_ROUTE")
    send_open_event_route = os.getenv("SEND_OPEN_EVENTS_ROUTE")
    opengate_user = os.getenv("OPENGATE_USER")
    opengate_password = os.getenv("OPENGATE_PASS")

    GPIO.setmode(GPIO.BCM)
    logger.info("Let's go")
    logger.info('start watchdog')
    watchdog = WatchDog(watchdog_com_port)
    logger.info('init database')
    data_base = DB()
    logger.info('init HTTP exchanging')
    http_getter = HttpGetter(data_base, opengate_server, opengate_port, open_codes_route, send_open_event_route, opengate_user, opengate_password)
    logger.info('init BAR scanner')
    scanner = BarScanner(bar_scanner_com_port, http_getter)
    logger.info('init barrier')
    barrier = Barrier(http_getter)
    http_getter.add_observer(barrier)
    led_assembly = LedAssembly(http_getter)

    keyboard_input = Keyboard(data_base)
    while BaseClass.working():
        sleep(1)