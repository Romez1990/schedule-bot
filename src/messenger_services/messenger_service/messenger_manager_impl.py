from typing import (
    Awaitable,
    NoReturn,
)

from data.fp.task import Task
from data.vector import List
from infrastructure.ioc_container import (
    Container,
    service,
)
from infrastructure.errors import NoReturnError
from .messenger_manager import MessengerManager
from .messenger_controller_registrar import MessengerControllerRegistrar
from .messenger_service import MessengerService


@service
class MessengerManagerImpl(MessengerManager):
    def __init__(self, messenger_controller_registrar: MessengerControllerRegistrar) -> None:
        self.__messenger_controller_registrar = messenger_controller_registrar

    def init(self, container: Container) -> None:
        self.__messenger_controller_registrar.register(container)

    async def start(self) -> NoReturn:
        tasks = List(self.__messenger_controller_registrar.messenger_services) \
            .map(self.__start_messenger_service)
        await Task.parallel(*tasks)
        raise NoReturnError

    def __start_messenger_service(self, messenger_service: MessengerService) -> Awaitable[NoReturn]:
        return messenger_service.start()
