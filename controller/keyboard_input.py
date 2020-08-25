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

    def set_level(self, level, level_class):
        if isinstance(level_class, str):
            _finded = False
            for cls in self.logger_level_classes:
                print(type(cls))
                if str(type(cls)).find(level_class) > -1:
                    level_class = cls
                    _finded = True
                    break
            if not _finded:
                print(f'class {level_class} not founded.')
                return

        if level == 'debug':
            level_class.set_debug()
        elif level == 'info':
            level_class.set_info()
        elif level == 'warning':
            level_class.set_warning()
        print(f'Set {level} log level for {level_class}')

    # Function of input in thread
    def read_kbd_input(self):
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
                            self.set_level(cmd_list[0], cmd_list[1])
                        else:
                            for cl in self.logger_level_classes:
                                self.set_level(cmd_list[0], cl)
                    elif 'exit' in cmd_list:
                        self.logger.info('Bye')
                        BaseClass.exit()
            except:
                continue