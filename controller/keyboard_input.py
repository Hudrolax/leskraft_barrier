import threading
import logging
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from model.http_getter import HttpGetter
from controller.barcode_scanner import BarScanner


class Keyboard(LoggerSuper):
    """
    Класс реализует поток чтение и обработку команд из консоли
    """
    logger = logging.getLogger('Keyboard')

    def __init__(self, db):
        # Start keyboart queue thread
        self._db = db
        self.logger_level_classes = [Keyboard, HttpGetter, BarScanner]
        self.inputThread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        self.inputThread.start()
        self.logger.info('start keyboard thread')

    # Function of input in thread
    def read_kbd_input(self):
        while BaseClass.working():
            # Receive keyboard input from user.
            try:
                input_str = input()
                print('Enter command: ' + input_str)
                cmd_list = input_str.split(' ')
                if 'codes' in cmd_list:
                    print(self._db.print_open_codes())
                elif 'debug' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_debug()
                        print(f'Set DEBUG log level for {cl}')
                elif 'info' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_info()
                        print(f'Set INFO log level for {cl}')
                elif 'warning' in cmd_list:
                    for cl in self.logger_level_classes:
                        cl.set_warning()
                        print(f'Set WARNING log level for {cl}')
                elif 'exit' in cmd_list:
                    self.logger.info('Bye')
                    BaseClass.exit()
            except:
                continue