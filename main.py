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
from model.telegram_bot import Telegram_bot
from RPi import GPIO


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    WRITE_LOG_TO_FILE = True
    LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
    LOG_LEVEL = logging.ERROR
    logger = logging.getLogger('main')

    if WRITE_LOG_TO_FILE:

        logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL,
                            datefmt='%d/%m/%y %H:%M:%S')
    else:
        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

    opengate_server = os.getenv("OPENGATE_SERVER")
    opengate_port = os.getenv("OPENGATE_PORT")
    open_codes_route = os.getenv("OPEN_CODES_ROUTE")
    send_open_event_route = os.getenv("SEND_OPEN_EVENTS_ROUTE")
    opengate_user = os.getenv("OPENGATE_USER")
    opengate_password = os.getenv("OPENGATE_PASS")
    bar_scanner_pid = os.getenv("BAR_SCANNER_PID")
    watchdog_pid = os.getenv("WATCHDOG_PID")
    telegram_api_token = os.getenv("TELEGRAM_API_TOKEN")
    telegram_bot_admins = os.getenv("ADMINS")

    GPIO.setmode(GPIO.BCM)
    logger.info("Let's go")
    logger.info('start watchdog')
    watchdog = WatchDog(watchdog_pid)
    logger.info('init database')
    data_base = DB()
    logger.info('init HTTP exchanging')
    http_getter = HttpGetter(data_base, opengate_server, opengate_port, open_codes_route, send_open_event_route, opengate_user, opengate_password)
    logger.info('init BAR scanner')
    scanner = BarScanner(bar_scanner_pid, http_getter)
    logger.info('init barrier')
    barrier = Barrier(http_getter)
    http_getter.add_observer(barrier)
    led_assembly = LedAssembly(http_getter)
    telegram_bot = Telegram_bot(telegram_api_token, barrier, telegram_bot_admins)

    keyboard_input = Keyboard(data_base, barrier)
    while BaseClass.working():
        sleep(1)