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
        self._closing_by_magnet_loop = True
        self._closing_by_timer = 0
        self._closing_by_timer_forcibly = 0

    def get_closing_by_timer(self):
        return self._closing_by_timer

    def get_closing_by_timer_forcibly(self):
        return self._closing_by_timer_forcibly

    def get_closing_by_magnet_loop(self):
        return self._closing_by_magnet_loop

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
        while True:
            try:
                self._get_open_codes()
                self.notify_observers()
                sleep(30)
            except Exception as e:
                print(f'_get_open_codes_thread_func: {e}')

    def _get_open_codes(self):
        try:
            response = requests.get(f"http://{self._server}:{self._port}{self._open_codes_route}", auth=(self._username, self._password), timeout=5)
            _answer = response.content.decode()
            self.logger.debug(f'get_open_codes answer: {_answer}')
            try:
                decoded_json = json.loads(_answer)
                self.logger.debug(f'Get JSON: {decoded_json}')
                _codelist = decoded_json.get('open_codes')
                _permissions_of_closing = decoded_json.get('permissions_of_closing')
                if _permissions_of_closing[0] == "true":
                    self._closing_by_magnet_loop = True
                    self.logger.debug(f'closing_by_magnet_loop = {self._closing_by_magnet_loop}')
                elif _permissions_of_closing[0] == "false":
                    self._closing_by_magnet_loop = False
                    self.logger.debug(f'closing_by_magnet_loop = {self._closing_by_magnet_loop}')

                try:
                    self._closing_by_timer = int(_permissions_of_closing[1])
                    self.logger.debug(f'_closing_by_timer = {self._closing_by_timer}')
                except:
                    self.logger.error(f'_get_open_codes type error. _permissions_of_closing[1] need integer, but {type(_permissions_of_closing[1])} got.')

                try:
                    self._closing_by_timer_forcibly = int(_permissions_of_closing[2])
                    self.logger.debug(f'closing_by_magnet_loop = {self._closing_by_timer_forcibly}')
                except:
                    self.logger.error(f'_get_open_codes type error. _permissions_of_closing[2] need integer, but {type(_permissions_of_closing[2])} got.')

                try:
                    self._db.open_codes = copy.deepcopy(_codelist)
                    self._db.commit()
                except:
                    self.logger.error('DB commit error!')
                self._last_connected_time = datetime.now()
            except:
                self.logger.error('Не смог распарсить JSON')
        except:
            self.logger.error(f'get_open_codes connection error to http://{self._server}:{self._port}{self._open_codes_route}')

    def _send_opening_event(self, code):
        try:
            response = requests.get(f"http://{self._server}:{self._port}{self._send_open_event_route}?barcode={code}",
                                    auth=(self._username, self._password))
            _answer = response.content.decode()
            self.logger.info(f'send_opening_event answer: {_answer}')
            print(f'send_opening_event answer: {_answer}')
        except:
            self.logger.error(
                f'send_opening_event connection error to http://{self._server}:{self._port}{self._send_open_event_route}')

    def get_permission_by_code(self, code):
        self.bool_get_permission = True
        if code in self._db.open_codes:
            self._permission = True
            self.notify_observers()
            self.logger.info(f'Получено разрешение на открытие по коду {code} в _db.open_codes')
            self._send_opening_event(code)
            sleep(2)
            self._permission = False
        else:
            self.logger.info(f'Отказано в разрешении на открытие по коду {code}')
            sleep(2)

    def reset_permission(self):
        self._permission = False

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()



if __name__ == '__main__':
    start = datetime.now()
    response = requests.get(f"http://{'85.172.104.127'}:{'8182'}{'/trade2019/hs/barrier/get_open_codes'}",
                            auth=('http_services', 'lk93295841lk'), timeout=5)
    finish = datetime.now()
    total = (finish - start).total_seconds()
    print(total)
    _answer = response.content.decode()