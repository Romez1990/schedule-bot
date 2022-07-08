from abc import ABCMeta, abstractmethod

from .message import Message


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def check(self, message: Message) -> bool: ...
