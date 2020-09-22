from utility.com_ports import COM_port
import threading
import logging
from datetime import datetime
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from time import sleep
from utility.reboot import reboot


class BarScanner(COM_port, LoggerSuper):
    """
    Класс BarScanner представляет собой реализацию модели сканера ШК.
    Класс оповещает наблюдателей о событии сканирования
    """
    logger = logging.getLogger('BarScanner')

    def __init__(self, PID, model):
        super().__init__(name='BarScanner', PID=PID, speed=9600, timeout=500)
        self.model = model
        self._thread = threading.Thread(target=self._get_bar_code_threaded, args=(), daemon=True)
        self._thread.start()

    def _get_bar_code_threaded(self):
        sleep(1)
        _last_barcode = None
        _time_last_wait_for_scan = datetime.now()
        _attempts = 0
        while BaseClass.working():
            _answer = ""
            if self.initialized:
                if _last_barcode != '':
                    self.logger.info('Wait for scan barcode...')
                try:
                    _answer = self.serial.readline().decode().replace('\n', '')
                    if _answer != '':
                        self.logger.info(f'{datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")}: {repr(_answer)}')
                        _attempts = 0
                except:
                    self.initialized = False
                    self.inicialize_com_port()
                if _answer != "":
                    if _answer.find('t=') == -1:
                        self.model.get_permission_by_code(_answer)
                    else:
                        self.logger.warning(f'Got wrong code format: {_answer}')
            else:
                sleep(0.2)
            if (datetime.now() - _time_last_wait_for_scan).total_seconds() < 1:
                _attempts += 1
            else:
                _attempts = 0
            _time_last_wait_for_scan = datetime.now()
            if _attempts > 50:
                print("need reboot")
                reboot()