import serial
import serial.tools.list_ports as lp
import threading
import logging
from datetime import datetime

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING

if WRITE_LOG_TO_FILE:
    logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')
else:
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

class BarScanner:
    """
    Класс BarScanner представляет собой реализацию модели сканера ШК.
    Класс оповещает модель о событии сканирования
    """
    logger = logging.getLogger('BarScanner')
    logger.setLevel(logging.DEBUG)
    def __init__(self, port, model):
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
        self._thread = threading.Thread(target=self._watch_port, args=(), daemon=True)
        self._thread.start()

    # Поток считывания данных со сканера и вызывает функцию у модели
    def _watch_port(self):
        while True:
            self.logger.debug('Wait for scan barcode...')
            _answer = self._com_port.readline().decode().replace('\n','')
            if _answer != "":
                self.logger.debug(f'{datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")}: {_answer}')
                self.model.get_permission_by_code(_answer)
