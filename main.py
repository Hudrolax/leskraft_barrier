import serial
import serial.tools.list_ports as lp

class BarScanner:
    def __init__(self, port):
        self._initialized = False
        _ports = list(lp.comports())
        for _port in _ports:
            if _port.device == port:
                self.port = serial.Serial(port.device, 115200)
                self._initialized = True
        if not self._initialized:
            raise Exception(f'ERROR!!! Port {port} does not exist')

    def watch_port(self):
        while True:
            _answer = self.port.readln()

if __name__ == '__main__':
    com_port = 'COM3'
    print('hello')
    scanner = BarScanner('COM3')
    _answer = scanner.port.readline()
    print(_answer)