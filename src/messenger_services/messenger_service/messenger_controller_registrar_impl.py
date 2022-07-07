from typing import (
    Sequence,
    Mapping,
    Callable,
    Type,
    Awaitable,
)

from infrastructure.ioc_container import service, Container
from data.vector import List
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
        controllers = self.__instantiate_controllers(container)
        self.__register_controllers(controllers)

    def __instantiate_controllers(self, container: Container
                                  ) -> Mapping[Type[MessengerController], Sequence[MessengerController]]:
        controllers_for_messengers = List(messenger_controllers) \
            .map(self.__instantiate_controller(container))
        return {controller_class: controllers
                for controller_class, controllers in zip(messenger_controllers, controllers_for_messengers)}

    def __instantiate_controller(self, container: Container
                                 ) -> Callable[[Type[MessengerController]], Sequence[MessengerController]]:
        def instantiate_controller(controller_class: Type[MessengerController]) -> Sequence[MessengerController]:
            return List(self.messenger_services) \
                .map(self.__instantiate_controller_for_messenger(container, controller_class))

        return instantiate_controller

    def __instantiate_controller_for_messenger(self, container: Container, controller_class: Type[MessengerController]
                                               ) -> Callable[[MessengerService], MessengerController]:
        def instantiate_controller_for_messenger(messenger_service: MessengerService) -> MessengerController:
            adapter = messenger_service.adapter
            additional_parameters = {
                'adapter': adapter,
            }
            return container.instantiate(controller_class, **additional_parameters)

        return instantiate_controller_for_messenger

    def __register_controllers(self,
                               controllers: Mapping[Type[MessengerController], Sequence[MessengerController]]) -> None:
        for parameters in message_handler_parameters:
            controllers_for_messengers = controllers[parameters.controller_class]
            self.__register_controllers_for_messengers(controllers_for_messengers, parameters)

    def __register_controllers_for_messengers(self, controllers: Sequence[MessengerController],
                                              parameters: MessageHandlerParameters) -> None:
        for messenger_service, controller in zip(self.messenger_services, controllers):
            adapter = messenger_service.adapter
            self.__register_message_handler_for_messenger(adapter, controller, parameters)

    def __register_message_handler_for_messenger(self, adapter: MessengerAdapter, controller: MessengerController,
                                                 parameters: MessageHandlerParameters) -> None:
        message_handler = self.__get_message_handler(controller, adapter, parameters.method_name)
        adapter.add_message_handler(parameters, message_handler)

    def __get_message_handler(self, controller: MessengerController, adapter: MessengerAdapter,
                              method_name: str) -> Callable[[object], Awaitable[None]]:
        method: Callable[[MessengerController, Message], Awaitable[None]] = getattr(controller, method_name)

        async def message_handler(messenger_message: object) -> None:
            message = adapter.map_message(messenger_message)
            await method(controller, message)

        return message_handler
