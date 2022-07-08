from typing import (
    Sequence,
    Callable,
    Type,
    Awaitable,
)

from infrastructure.ioc_container import service, Container
from messenger_services.telegram_service import TelegramService
from messenger_services.vk_service import VkService
from .structures import (
    Message,
    MessageHandlerParameters,
)
from .messenger_controller_registrar import MessengerControllerRegistrar
from .messenger_service import MessengerService
from .messenger_adapter import MessengerAdapter
from .messenger_controller import MessengerController
from .controller_decorator import messenger_controllers
from .message_handler_decorator import message_handler_parameters


@service
class MessengerControllerRegistrarImpl(MessengerControllerRegistrar):
    def __init__(self, telegram: TelegramService,
                 vk: VkService) -> None:
        self.messenger_services: Sequence[MessengerService] = [
            telegram,
            vk,
        ]

    def register(self, container: Container) -> None:
        controllers = self.__create_controllers(container)
        for messenger_service in self.messenger_services:
            controllers_for_messenger_service = controllers[type(messenger_service)]
            for parameters in message_handler_parameters:
                controller = controllers_for_messenger_service[parameters.controller_class]
                self.__register_message_handler_for_messenger_service(messenger_service, controller, parameters)

    def __create_controllers(self, container: Container
                             ) -> dict[Type[MessengerService], dict[Type[MessengerController], MessengerController]]:
        controllers = {}
        for messenger_service in self.messenger_services:
            controllers_for_messenger_service = {}
            for controller_class in messenger_controllers:
                adapter = messenger_service.adapter
                additional_parameters = {
                    'adapter': adapter,
                }
                controller = container.instantiate(controller_class, **additional_parameters)
                controllers_for_messenger_service[controller_class] = controller
            controllers[type(messenger_service)] = controllers_for_messenger_service
        return controllers

    def __register_message_handler_for_messenger_service(
            self, messenger_service: MessengerService, controller: MessengerController,
            parameters: MessageHandlerParameters) -> None:
        adapter = messenger_service.adapter
        message_handler = self.__get_message_handler(controller, adapter, parameters.method_name)
        adapter.add_message_handler(parameters, message_handler)

    def __get_message_handler(self, controller: MessengerController, adapter: MessengerAdapter,
                              method_name: str) -> Callable[[object], Awaitable[None]]:
        method: Callable[[MessengerController, Message], Awaitable[None]] = getattr(controller, method_name)

        async def message_handler(messenger_message: object) -> None:
            message = adapter.map_message(messenger_message)
            await method(controller, message)

        return message_handler
