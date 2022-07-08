from typing import (
    MutableSequence,
    Callable,
    Type,
    TypeVar,
    Awaitable,
)

from infrastructure.decorator import (
    check_decorating_callable,
    check_decorating_class,
    check_decorating_class_name,
)
from .structures import (
    Message,
    Callback,
    Payload,
    MessageHandlerParamsForRegistrar,
    CallbackHandlerParamsForRegistrar,
)
from .messenger_controller import MessengerController

messenger_controllers: MutableSequence[Type[MessengerController]] = []
TController = TypeVar('TController', bound=MessengerController)


def controller(class_type: Type[TController]) -> Type[TController]:
    check_decorating_class(controller, MessengerController, class_type)
    check_decorating_class_name(class_type, 'Controller')
    messenger_controllers.append(class_type)
    return class_type


message_handler_params: MutableSequence[MessageHandlerParamsForRegistrar] = []


def message_handler(command: str) -> type:
    class MessageHandler:
        def __init__(self, method: Callable[[MessengerController, Message], Awaitable[None]]) -> None:
            check_decorating_callable(message_handler, method)
            self.__method = method

        def __set_name__(self, owner: Type[MessengerController], name: str) -> None:
            message_handler_params.append(MessageHandlerParamsForRegistrar(owner, name, command))

        async def __call__(self, messenger_controller: MessengerController, message: Message) -> None:
            await self.__method(messenger_controller, message)

    return MessageHandler


callback_handler_params: MutableSequence[CallbackHandlerParamsForRegistrar] = []


def callback_handler(payload_class: Type[Payload]) -> type:
    class CallbackHandler:
        def __init__(self, method: Callable[[MessengerController, Callback, Payload], Awaitable[None]]) -> None:
            check_decorating_callable(callback_handler, method)
            self.__method = method

        def __set_name__(self, owner: Type[MessengerController], name: str) -> None:
            callback_handler_params.append(CallbackHandlerParamsForRegistrar(owner, name, payload_class))

        async def __call__(self, messenger_controller: MessengerController, callback: Callback,
                           payload: Payload) -> None:
            await self.__method(messenger_controller, callback, payload)

    return CallbackHandler
