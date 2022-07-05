from typing import (
    Type,
    Awaitable,
    NoReturn,
)

from infrastructure.ioc_container import service, Container
from infrastructure.errors import NoReturnError
from data.fp.task import Task
from data.vector import List
from messenger_services.telegram_service import TelegramService
from messenger_services.vk_service import VkService
from .structures import (
    MessageHandlerParameters,
)
from .message_handler_registrar import MessageHandlerRegistrar
from .controller_decorator import messenger_controllers
from .message_handler_adapter import MessageHandlerAdapter
from .messenger_controller import MessengerController
from .messenger_service import MessengerService
from .message_handler_decorator import message_handler_parameters


@service
class MessageHandlerRegistrarImpl(MessageHandlerRegistrar):
    def __init__(self, message_handler_adapter: MessageHandlerAdapter, telegram: TelegramService,
                 vk: VkService) -> None:
        self.__message_handler_adapter = message_handler_adapter
        self.__messenger_services: list[MessengerService] = [
            telegram,
            vk,
        ]

    def register(self, container: Container) -> None:
        controllers = self.__create_controllers(container)
        for messenger_service in self.__messenger_services:
            controllers_for_messenger_service = controllers[type(messenger_service)]
            for parameters in message_handler_parameters:
                controller = controllers_for_messenger_service[parameters.controller_class]
                self.__register_message_handler_for_messenger_service(messenger_service, controller, parameters)

    def __create_controllers(self, container: Container
                             ) -> dict[Type[MessengerService], dict[Type[MessengerController], MessengerController]]:
        controllers = {}
        for messenger_service in self.__messenger_services:
            controllers_for_messenger_service = {}
            for controller_class in messenger_controllers:
                adapter = messenger_service.adapter
                additional_parameters = {
                    'adapter': adapter,
                }
                controller = container.create(controller_class, **additional_parameters)
                controllers_for_messenger_service[controller_class] = controller
            controllers[type(messenger_service)] = controllers_for_messenger_service
        return controllers

    def __register_message_handler_for_messenger_service(
            self, messenger_service: MessengerService, controller: MessengerController,
            parameters: MessageHandlerParameters) -> None:
        adapter = messenger_service.adapter
        message_handler = self.__message_handler_adapter.get_message_handler(controller, adapter,
                                                                             parameters.method_name)
        messenger_service.add_message_handler(parameters, message_handler)

    async def start(self) -> NoReturn:
        tasks = List(self.__messenger_services) \
            .map(self.__start_messenger_service)
        await Task.parallel(tasks)
        raise NoReturnError

    def __start_messenger_service(self, messenger_service: MessengerService) -> Awaitable[NoReturn]:
        return messenger_service.start()
