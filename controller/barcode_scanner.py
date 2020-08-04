import serial
import serial.tools.list_ports as lp
import threading
import logging
from datetime import datetime
from utility.logger_super import LoggerSuper
from time import sleep

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING

if WRITE_LOG_TO_FILE:
    logging.basicConfig(filename='leskraft_barrier.txt', filemode='w', format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')
else:
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt='%d/%m/%y %H:%M:%S')

class BarScanner(LoggerSuper):
    """
    Класс BarScanner представляет собой реализацию модели сканера ШК.
    Класс оповещает модель о событии сканирования
    """
    logger = logging.getLogger('BarScanner')

    def __init__(self, port, model):
        self.model = model
        self._port = port
        self._com_port = None
        self._initialized = False
        self._inicialize_com_port()
        self._thread = threading.Thread(target=self._get_bar_code_threaded, args=(), daemon=True)
        self._thread.start()

    def _inicialize_com_port(self):
        if not self._initialized:
            try:
                self._com_port.close()
            except:
                pass
            _ports = list(lp.comports())
            for _port in _ports:
                if _port.device == self._port:
                    self._com_port = serial.Serial(_port.device, 9600, timeout=60)
                    self._initialized = True
            if not self._initialized:
                self.logger.critical(f'ERROR!!! Port {self._port} does not exist')
                raise Exception(f'ERROR!!! Port {self._port} does not exist')

    def _get_bar_code_threaded(self):
        while True:
            if self._initialized:
                self.logger.info('Wait for scan barcode...')
                try:
                    _answer = self._com_port.readline().decode().replace('\n', '')
                    self.logger.info(f'{datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")}: {repr(_answer)}')
                except:
                    self._inicialize_com_port()
                    continue
                if _answer != "":
                    self.model.get_permission_by_code(_answer)
            else:
                sleep(0.5)
