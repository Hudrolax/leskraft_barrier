from abc import ABCMeta, abstractmethod

class Observer(metaclass = ABCMeta):
    """
    Абстрактный суперкласс для всех наблюдателей.
    """
    @abstractmethod
    def modelIsChanged(self):
        """
        Метод который будет вызван у наблюдателя при изменении модели.
        """
        pass

class LoggerMeta(metaclass = ABCMeta):
    """
    Абстрактный суперкласс для всех логгированных классов.
    """
    @abstractmethod
    @staticmethod
    def set_debug():
        pass

    @abstractmethod
    @staticmethod
    def set_info():
        pass

    @abstractmethod
    @staticmethod
    def set_warning():
        pass