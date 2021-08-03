from typing import (
    Callable,
    Awaitable,
    TypeVar,
)

from infrastructure.ioc_container import service
from .message_handler_adapter import MessageHandlerAdapter
from .messenger_controller import MessengerController
from .messenger_adapter import MessengerAdapter
from .message import Message

T = TypeVar('T')


@service
class MessageHandlerAdapterImpl(MessageHandlerAdapter):
    def get_message_handler(self, controller: MessengerController, adapter: MessengerAdapter,
                            method_name: str) -> Callable[[object], Awaitable[None]]:
        method: Callable[[MessengerController, Message], Awaitable[None]] = getattr(controller, method_name)

        async def message_handler(messenger_message: T) -> None:
            message = adapter.map_message(messenger_message)
            await method(controller, message)

        return message_handler
