from utility.observer import Observer
import serial
import serial.tools.list_ports as lp
from time import sleep

import logging

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING

if WRITE_LOG_TO_FILE:
    logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')
else:
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

class ArduinoBarrier(Observer):
    logger = logging.getLogger('ArduinoBarrier')
    logger.setLevel(logging.DEBUG)
    def __init__(self, model, port='COM4'):
        self.model = model
        self._initialized = False
        self._com_port = None
        _ports = list(lp.comports())
        for _port in _ports:
            if _port.device == port:
                self._com_port = serial.Serial(_port.device, 115200)
                self._initialized = True
        if not self._initialized:
            self.logger.critical(f'ERROR!!! Port {port} does not exist')
            raise Exception(f'ERROR!!! Port {port} does not exist')

    def open(self):
        self._com_port.write('cmd=90\r'.encode())
        self.logger.debug('открыл шлагбаум')

    def close(self):
        self._com_port.write('cmd=0\r'.encode())
        self.logger.debug('закрыл шлагбаум')

    def modelIsChanged(self):
        if self.model is None or self.model is not None and self.model.permission:
            self.open()
            sleep(20)
            self.close()

if __name__ == '__main__':
    barrier = ArduinoBarrier(None, 'COM4')
    print('opening')
    barrier.open()
    sleep(5)
    print('closing')
    barrier.close()