import logging
import requests
import json
from time import sleep
import threading
import copy
from utility.observer import LoggerMeta

WRITE_LOG_TO_FILE = False
LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.WARNING

class HttpGetter(LoggerMeta):
    """
    Класс описывает объект, который запрашивает разрешение на открытие шлагбаума
    в центральной базе по роуту, передавая отcканированный ШК
    """
    logger = logging.getLogger('HttpGetter')
    logger.setLevel(logging.INFO)

    @staticmethod
    def set_debug():
        HttpGetter.logger.setLevel(logging.DEBUG)

    @staticmethod
    def set_info():
        HttpGetter.logger.setLevel(logging.INFO)

    @staticmethod
    def set_warning():
        HttpGetter.logger.setLevel(logging.WARNING)

    def __init__(self, db, server, port, open_codes_route, send_open_event_route, user, password):
        self._observers = []
        self._db = db
        self._server = server
        self._port = port
        self._open_codes_route = open_codes_route
        self._send_open_event_route = send_open_event_route
        self._username = user
        self._password = password
        self._permission = False
        self._get_open_codes_thread = threading.Thread(target=self._get_open_codes_thread_func, args=(), daemon=True)
        self._get_open_codes_thread.start()

    @property
    def permission(self):
        return self._permission

    def _get_open_codes_thread_func(self):
        while True:
            self._get_open_codes()
            sleep(5)

    def _get_open_codes(self):
        try:
            response = requests.get(f"http://{self._server}:{self._port}{self._open_codes_route}", auth=(self._username, self._password))
            _answer = response.content.decode()
            self.logger.debug(f'get_open_codes answer: {_answer}')
            try:
                decoded_json = json.loads(_answer)
                self.logger.debug(f'Get JSON: {decoded_json}')
                _codelist = decoded_json.get('open_codes')
                self._db.admin_codes = copy.deepcopy(_codelist)
                self._db.commit()
            except:
                self.logger.error('Не смог распарсить JSON')
        except:
            self.logger.error(f'get_open_codes connection error to http://{self._server}gg:{self._port}{self._open_codes_route}')

    def _send_opening_event(self, code):
        try:
            response = requests.get(f"http://{self._server}:{self._port}{self._send_open_event_route}?barcode={code}",
                                    auth=(self._username, self._password))
            _answer = response.content.decode()
            self.logger.debug(f'send_opening_event answer: {_answer}')
        except:
            self.logger.error(
                f'send_opening_event connection error to http://{self._server}:{self._port}{self._send_open_event_route}')

    def get_permission_by_code(self, code):
        if code in self._db.admin_codes:
            self._permission = True
            self.logger.info(f'Получено разрешение на открытие по коду {code} в _db.admin_codes')
            self.notify_observers()
            self._send_opening_event(code)
        else:
            self.logger.info(f'Отказано в разрешении на открытие по коду {code}')
        self._permission = False

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.modelIsChanged()

if __name__ == '__main__':
    bar_scanner_com_port = 'COM3'
    opengate_server = 'golden1'
    opengate_port = '80'
    opengate_route = '/trade2016donate/hs/barrier/get_perrmission'
    admin_codes_route = '/trade2016donate/hs/barrier/get_admin_codes'
    opengate_user = 'http_services'
    opengate_password = 'lk93295841lk'
    from model.data_base import DB
    data_base = DB()
    http_getter = HttpGetter(data_base, opengate_server, opengate_port, opengate_route, admin_codes_route, opengate_user, opengate_password)
    http_getter.get_admin_codes()
    print(data_base.print_admin_codes())
