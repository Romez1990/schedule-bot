from typing import (
    Callable,
    Awaitable,
)
from vkwave.bots import (
    SimpleLongPollUserBot,
    SimpleUserEvent,
)
from vkwave.types.user_events import MessageEventObject

from messenger_services.messenger_service import MessengerAdapter, MessageHandlerParameters, Message, User


class VkWaveAdapter(MessengerAdapter[SimpleUserEvent]):
    def __init__(self, bot: SimpleLongPollUserBot) -> None:
        self.__bot = bot
        self.__api_context = self.__bot.api_context

    async def send_message(self, user: User, text: str, keyboard=None) -> None:
        await self.__api_context.messages.send(peer_id=user.chat_id, message=text, random_id=0)

    async def send_image(self, user: User, image_bytes: bytes) -> None:
        raise RuntimeError

    def map_message(self, message: SimpleUserEvent) -> Message:
        event = message.object.object
        user = self.__map_user(event)
        return Message(user, event.text)

    def __map_user(self, event: MessageEventObject) -> User:
        return User(event.peer_id)

    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[SimpleUserEvent], Awaitable[None]]) -> None:
        self.__bot.message_handler(self.__bot.command_filter([parameters.command], prefixes=['/', '']))(method)
