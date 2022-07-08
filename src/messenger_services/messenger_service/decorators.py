from typing import (
    MutableSequence,
    Callable,
    Type,
    TypeVar,
    Awaitable,
)

from infrastructure.decorator import (
    check_decorating_callable,
    check_decorating_type,
    check_decorating_class_name,
)
from .structures import (
    Message,
    MessageHandlerParameters,
)
from .messenger_controller import MessengerController

messenger_controllers: MutableSequence[Type[MessengerController]] = []
TController = TypeVar('TController', bound=MessengerController)


def controller(class_type: Type[TController]) -> Type[TController]:
    check_decorating_type(controller, MessengerController, class_type)
    check_decorating_class_name(class_type, 'Controller')
    messenger_controllers.append(class_type)
    return class_type


message_handler_parameters: MutableSequence[MessageHandlerParameters] = []


def message_handler(command: str) -> type:
    class MessageHandler:
        def __init__(self, method: Callable[[MessengerController, Message], Awaitable[None]]) -> None:
            check_decorating_callable(message_handler, method)
            self.__method = method

        def __set_name__(self, owner: Type[MessengerController], name: str) -> None:
            message_handler_parameters.append(MessageHandlerParameters(owner, name, command))

        async def __call__(self, messenger_controller: MessengerController, message: Message) -> None:
            await self.__method(messenger_controller, message)

    return MessageHandler
