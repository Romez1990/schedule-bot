from abc import ABCMeta, abstractmethod

from infrastructure.ioc_container import Container


class MessengerControllerRegistrar(metaclass=ABCMeta):
    @abstractmethod
    def register(self, container: Container) -> None: ...
