from typing import (
    Callable,
    Awaitable,
    Type,
)

from infrastructure.decorator import (
    check_decorating_callable,
)
from .message import Message
from .messenger_controller import MessengerController
from .messege_handler_parameters import MessageHandlerParameters

message_handler_parameters: list[MessageHandlerParameters] = []


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
