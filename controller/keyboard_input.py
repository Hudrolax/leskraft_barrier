import threading
import logging
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from model.http_getter import HttpGetter
from view.barrier import Barrier
from controller.barcode_scanner import BarScanner


class Keyboard(LoggerSuper):
    """
    Класс реализует поток чтение и обработку команд из консоли
    """
    logger = logging.getLogger('Keyboard')

    def __init__(self, db, barrier):
        # Start keyboart queue thread
        self._db = db
        self._barrier = barrier
        self.logger_level_classes = [Keyboard, HttpGetter, BarScanner, Barrier]
        self.inputThread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        self.inputThread.start()
        self.logger.info('start keyboard thread')

    def set_level(self, level, level_class):
        if isinstance(level_class, str):
            _finded = False
            for cls in self.logger_level_classes:
                   if str(cls).find(level_class) > -1:
                    level_class = cls
                    _finded = True
                    break
            if not _finded:
                print(f'class {level_class} not found.')
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
                    elif 'settings' in cmd_list:
                        _settings = 'Settings:\n'
                        _settings += f'Closing by magnet loop: {self._barrier.get_closing_by_magnet_loop()}\n'
                        _settings += f'Magnet loop delay: {self._barrier.get_magnet_loop_delay()} sec.\n'
                        _settings += f'Closing by timer delay: {self._barrier.get_timer_delay()} sec.\n'
                        _settings += f'Closing forcibly by timer selay: {self._barrier.get_timer_delay_forcibly()} sec.\n'
                        print(_settings)
                    elif 'open' in cmd_list:
                        self._barrier.open()
                        print('opened by keyboard...')
                    elif 'close' in cmd_list:
                        self._barrier.close()
                        print('closed by keyboard...')
                    elif 'exit' in cmd_list:
                        self.logger.info('Bye')
                        BaseClass.exit()
            except:
                continue