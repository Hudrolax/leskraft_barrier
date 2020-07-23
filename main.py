import serial
import serial.tools.list_ports as lp

class BarScanner:
    def __init__(self, port):
        self.port = serial.Serial(port, 115200, timeout=1)

    def watch_port(self):
        while True:
            _answer = self.port.readln()

if __name__ == '__main__':
    print('hello')
    scanner = BarScanner('COM3')
    _answer = scanner.port.readln()
    print(_answer)