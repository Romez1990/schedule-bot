from typing import (
    Sequence,
    Mapping,
    Callable,
    Type,
    TypeVar,
    ParamSpec,
    Concatenate,
    Awaitable,
)

from infrastructure.ioc_container import service, Container
from data.vector import List
from messenger_services.telegram_service import TelegramService
from messenger_services.vk_service import VkService
from .structures import (
    Message,
    MessageHandlerParamsForRegistrar,
    HandlerParamsForRegistrar,
)
from .messenger_controller_registrar import MessengerControllerRegistrar
from .messenger_service import MessengerService
from .messenger_adapter import MessengerAdapter
from .messenger_controller import MessengerController
from .decorators import (
    messenger_controllers,
    message_handler_params,
)

TParams = TypeVar('TParams', bound=HandlerParamsForRegistrar)
P = ParamSpec('P')


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
        self.__register_handlers(controllers, message_handler_params, self.__register_message_handler)

    def __register_handlers(self,
                            controllers: Mapping[Type[MessengerController], Sequence[MessengerController]],
                            all_params: Sequence[TParams],
                            register_handler: Callable[[MessengerController, MessengerAdapter, TParams], None]) -> None:
        for params in all_params:
            controllers_for_messengers = controllers[params.controller_class]
            self.__register_handler(controllers_for_messengers, params, register_handler)

    def __register_handler(self, controllers: Sequence[MessengerController], params: TParams,
                           register_handler: Callable[[MessengerController, MessengerAdapter, TParams], None]) -> None:
        for messenger_service, controller in zip(self.messenger_services, controllers):
            adapter = messenger_service.adapter
            register_handler(controller, adapter, params)

    def __register_message_handler(self, controller: MessengerController, adapter: MessengerAdapter,
                                   params: MessageHandlerParamsForRegistrar) -> None:
        handler: Callable[[Message], Awaitable[None]] = self.__get_method(controller, params.method_name)
        adapter.register_message_handler(params, handler)

    def __get_method(self, controller: MessengerController, method_name: str) -> Callable[P, Awaitable[None]]:
        method: Callable[Concatenate[MessengerController, P], Awaitable[None]] = getattr(controller, method_name)
        return self.__method_to_function(controller, method)

    def __method_to_function(self, controller: MessengerController,
                             method: Callable[Concatenate[MessengerController, P], Awaitable[None]]
                             ) -> Callable[P, Awaitable[None]]:
        async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
            await method(controller, *args, **kwargs)

        return handler
