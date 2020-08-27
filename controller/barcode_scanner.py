import serial
import serial.tools.list_ports as lp
import threading
import logging
from datetime import datetime
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from time import sleep


class BarScanner(LoggerSuper):
    """
    Класс BarScanner представляет собой реализацию модели сканера ШК.
    Класс оповещает наблюдателей о событии сканирования
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
        self.logger.info('BarScanner initialized at port ' + self._port)

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
        sleep(1)
        _last_barcode = None
        while BaseClass.working():
            if self._initialized:
                if _last_barcode != '':
                    self.logger.info('Wait for scan barcode...')
                try:
                    _answer = self._com_port.readline().decode().replace('\n', '')
                    if _answer != '':
                        self.logger.info(f'{datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")}: {repr(_answer)}')
                except:
                    self._inicialize_com_port()
                    continue
                if _answer != "":
                    self.model.get_permission_by_code(_answer)
            else:
                sleep(0.2)
