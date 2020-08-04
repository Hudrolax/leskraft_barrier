from utility.observer import Observer
import serial
import serial.tools.list_ports as lp
from utility.logger_super import LoggerSuper
from time import sleep
import logging


class ArduinoBarrier(Observer, LoggerSuper):
    """
    Класс описывает управление arduino-шлагбаумом (макетный вариант)
    """
    logger = logging.getLogger('ArduinoBarrier')

    def __init__(self, model, port='COM4'):
        self._port = port
        self._com_port = None
        self.model = model
        self._initialized = False
        self._inicialize_arduino()


    def _inicialize_arduino(self):
        if not self._initialized:
            try:
                self._com_port.close()
            except:
                pass
            self._com_port = None
            _ports = list(lp.comports())
            for _port in _ports:
                if _port.device == self._port:
                    self._com_port = serial.Serial(_port.device, 115200)
                    self._initialized = True
            if not self._initialized:
                self.logger.critical(f'ERROR!!! Port {self._port} does not exist')
                raise Exception(f'ERROR!!! Port {self._port} does not exist')

    def open(self):
        try:
            self._com_port.write('cmd=90\r'.encode())
            self.logger.debug('открыл шлагбаум')
        except:
            self.logger.error('Что-то c макетом шлагбаума. Не смог отправить команду ОТКРЫТЬ')
            self._inicialize_arduino()

    def close(self):
        try:
            self._com_port.write('cmd=0\r'.encode())
            self.logger.debug('закрыл шлагбаум')
        except:
            self.logger.error('Что-то c макетом шлагбаума. Не смог отправить команду ЗАКРЫТЬ')
            self._inicialize_arduino()

    def modelIsChanged(self):
        self.open()
        sleep(5)
        self.close()

if __name__ == '__main__':
    barrier = ArduinoBarrier(None, 'COM4')
    print('opening')
    barrier.open()
    sleep(5)
    print('closing')
    barrier.close()