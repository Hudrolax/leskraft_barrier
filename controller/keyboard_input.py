import threading
import logging

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING


class Keyboard:
    logger = logging.getLogger('Keyboard')
    logger.setLevel(logging.DEBUG)
    def __init__(self, db):
        # Start keyboart queue thread
        self._db = db
        self.inputThread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        self.inputThread.start()
        self.logger.info('start keyboard thread')

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
            except:
                continue