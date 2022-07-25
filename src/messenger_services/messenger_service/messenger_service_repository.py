from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from messenger_services.messenger_service import MessengerService


class MessengerServiceRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> Sequence[MessengerService]: ...
