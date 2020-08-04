import serial
import threading
from time import sleep
from utility.logger_super import LoggerSuper
import logging


class WatchDog(LoggerSuper):
    logger = logging.getLogger('CWatchDog')

    def __init__(self, port):
        self.port = port  # порт подключения вотчдога
        self.logger.info('Try connect to WatchDog at port ' + self.port)
        self._serial = serial.Serial(self.port, 9600, timeout=1)  # change ACM number as found from ls /dev/tty/ACM*
        self._serial.flushInput()
        self._serial.flushOutput()
        self._serial.baudrate = 9600
        self._serial.timeout = 1
        self._serial.write_timeout = 1
        self._watchdog_thread = threading.Thread(target=self._ping, args=(), daemon=True)
        self._watchdog_thread.start()

    @staticmethod
    def _send_to_serial(_s_port, s):
        try:
            _s_port.write(bytes(s, 'utf-8'))
        except:
            CWatchDog.logger.debug(f'Write error to port {_s_port}')

    def _ping(self):
        while True:
            self._send_to_serial(self._serial, '~U')  # Отправка команды "я в норме" на вотчдог
            sleep(3)