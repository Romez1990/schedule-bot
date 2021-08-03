from abc import ABCMeta, abstractmethod

from .connection import Connection


class ConnectionFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self) -> Connection: ...
