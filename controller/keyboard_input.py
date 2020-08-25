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
        def set_level(level, level_class):
            if isinstance(level_class, str):
                for cls in self.logger_level_classes:
                    if str(type(cls)).find('level_class'):
                        level_class = cls
                        break

            if level == 'debug':
                level_class.set_debug()
            elif level == 'info':
                level_class.set_info()
            elif level == 'warning':
                level_class.set_warning()
            print(f'Set {level} log level for {level_class}')

        while BaseClass.working():
            # Receive keyboard input from user.
            try:
                input_str = input()
                print('Enter command: ' + input_str)
                cmd_list = input_str.split(' ')
                if len(cmd_list) > 0:
                    if 'codes' in cmd_list:
                        print(self._db.print_open_codes())
                    elif 'debug' == cmd_list[0] or 'info' == cmd_list[0] or 'warning' == cmd_list[0]:
                        if len(cmd_list) == 2:
                            set_level(cmd_list[0], cmd_list[1])
                        else:
                            for cl in self.logger_level_classes:
                                set_level(cmd_list[0], cl)
                    elif 'exit' in cmd_list:
                        self.logger.info('Bye')
                        BaseClass.exit()
            except:
                continue