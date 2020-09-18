from utility.com_ports import COM_port
import threading
from time import sleep
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
import logging


class WatchDog(LoggerSuper, BaseClass, COM_port):
    logger = logging.getLogger('CWatchDog')

    def __init__(self, PID):
        super().__init__('WatchDog', PID, 9600, 1)

        self._watchdog_thread = threading.Thread(target=self._ping, args=(), daemon=True)
        self._watchdog_thread.start()

    @classmethod
    def _send_to_serial(cls, _s_port, s):
        try:
            _s_port.write(bytes(s, 'utf-8'))
        except:
            cls.logger.warning(f'Write error to port {_s_port}')

    def _ping(self):
        while self.working():
            self._send_to_serial(self.serial, '~U')  # Отправка команды "я в норме" на вотчдог
            sleep(3)