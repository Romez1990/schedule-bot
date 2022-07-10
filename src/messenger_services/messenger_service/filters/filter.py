from abc import ABCMeta, abstractmethod

from messenger_services.messenger_service import (
    Callback,
)


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def check(self, callback: Callback) -> bool: ...
