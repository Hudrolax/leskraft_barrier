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
    @staticmethod
    @abstractmethod
    def set_debug():
        pass

    @staticmethod
    @abstractmethod
    def set_info():
        pass

    @staticmethod
    @abstractmethod
    def set_warning():
        pass