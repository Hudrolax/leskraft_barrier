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
    def set_debug(self):
        pass

    @abstractmethod
    def set_info(self):
        pass

    @abstractmethod
    def set_warning(self):
        pass