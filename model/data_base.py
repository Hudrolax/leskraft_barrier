import sqlite3 as sql
import threading
from time import sleep

class DB:
    """
    Класс описывает объект базы данных для ведения кодов ШК
    Класс реализует запись и чтение БД в собственном потоке
    """
    def __init__(self):
        self._init = False
        self._sql_thread = threading.Thread(target=self._threaded_sql_func, args=(), daemon=True)
        self._sql_thread.start()
        self.connection = None
        self.open_codes = []
        self._commit = False
        while not self._init:
            sleep(0.1)

    def commit(self):
        self._commit = True

    def find_code(self, code):
        return code in self.open_codes

    def print_open_codes(self):
        answer = 'open_codes:\n'
        for code in self.open_codes:
            answer += code + '\n'
        return answer

    def _threaded_sql_func(self):
        self.connection = sql.connect('base.sqlite')
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS admin_codes (code text)''')
            self.connection.commit()
            cur.close()
        self._load_codes_from_db()
        self._init = True
        while True:
            if self._commit:
                self._update_open_codes()
                self._commit = False
            else:
                sleep(0.1)

    def _load_codes_from_db(self):
        self.open_codes = []
        cur = self.connection.cursor()
        cur.execute(f'''SELECT code FROM admin_codes''')
        _list = cur.fetchall()
        for el in _list:
            self.open_codes.append(el[0])

    def _update_open_codes(self):
        cur = self.connection.cursor()
        cur.execute(f'''DELETE FROM admin_codes''')
        for code in self.open_codes:
            cur.execute(f'''INSERT INTO admin_codes VALUES ({code})''')
        self.connection.commit()
        cur.close()

    def _find_code_from_db(self, code):
        _code = str(code)
        cur = self.connection.cursor()
        cur.execute(f'''SELECT code FROM admin_codes WHERE code=?''', (_code,))
        if len(cur.fetchall()) > 0:
            return True
        return False

    def _print_open_codes_from_db(self):
        answer = 'open_codes:\n'
        cur = self.connection.cursor()
        cur.execute(f"SELECT * FROM `admin_codes`")
        rows = cur.fetchall()
        for row in rows:
            answer += row[0] + '\n'
        cur.close()
        return answer


if __name__ == '__main__':
    code_list = ['111', '222', '333']
    data_base = DB()
    print(data_base.print_admin_codes())
    print(data_base.find_code('2422'))

