from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from infrastructure.ioc_container import Container
from .messenger_service import MessengerService


class MessengerControllerRegistrar(metaclass=ABCMeta):
    messenger_services: Sequence[MessengerService]

    @abstractmethod
    def register(self, container: Container) -> None: ...
