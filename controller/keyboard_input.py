import threading
import logging
from utility.observer import LoggerMeta
from model.http_getter import HttpGetter
from controller.barcode_scanner import BarScanner

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING


class Keyboard(LoggerMeta):
    logger = logging.getLogger('Keyboard')
    logger.setLevel(logging.DEBUG)
    def __init__(self, db):
        # Start keyboart queue thread
        self._db = db
        self.logger_level_classes = [self, HttpGetter, BarScanner]
        self.inputThread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        self.inputThread.start()
        self.logger.info('start keyboard thread')

    def set_debug(self):
        self.logger.setLevel(logging.DEBUG)

    def set_info(self):
        self.logger.setLevel(logging.INFO)

    def set_warning(self):
        self.logger.setLevel(logging.WARNING)

    # Function of input in thread
    def read_kbd_input(self):
        while True:
            # Receive keyboard input from user.
            try:
                input_str = input()
                print('Enter command: ' + input_str)
                cmd_list = input_str.split(' ')
                if 'admins' in cmd_list:
                    print(self._db.print_admin_codes())
                elif 'debug' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_debug()
                elif 'info' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_info()
                elif 'warning' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_warning()
            except:
                continue