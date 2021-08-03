from abc import ABCMeta, abstractmethod

from .logger import Logger


class LoggerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, module_name: str = None) -> Logger: ...
