import logging
import requests
import json
from time import sleep
import threading
import copy
from utility.logger_super import LoggerSuper
from utility.base_class import BaseClass
from datetime import datetime


class HttpGetter(LoggerSuper):
    """
    Класс описывает объект, который запрашивает список ШК из центральной базы и выдает разрешение на открытие шлагбаума
    """
    logger = logging.getLogger('HttpGetter')

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
        self._last_connected_time = datetime.now()
        self._get_open_codes_thread = threading.Thread(target=self._get_open_codes_thread_func, args=(), daemon=True)
        self._get_open_codes_thread.start()
        self.bool_get_permission = False

    @property
    def connected(self):
        if (datetime.now() - self._last_connected_time).total_seconds() < 10:
            return True
        else:
            return False

    @property
    def permission(self):
        return self._permission

    def _get_open_codes_thread_func(self):
        while BaseClass.working():
            self._get_open_codes()
            self.notify_observers()
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
                self._db.open_codes = copy.deepcopy(_codelist)
                self._db.commit()
            except:
                self.logger.error('Не смог распарсить JSON')

            self._last_connected_time = datetime.now()
        except:
            self.logger.error(f'get_open_codes connection error to http://{self._server}:{self._port}{self._open_codes_route}')

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
        self.bool_get_permission = True
        if code in self._db.open_codes:
            self._permission = True
            self.logger.info(f'Получено разрешение на открытие по коду {code} в _db.open_codes')
            self._send_opening_event(code)
        else:
            self.logger.info(f'Отказано в разрешении на открытие по коду {code}')

    def reset_permission(self):
        self._permission = False

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()
