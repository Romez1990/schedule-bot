from typing import (
    Callable,
    Awaitable,
)
from vkbottle.bot import (
    Bot,
    Message as VkMessage,
)
from vkbottle.dispatch.rules.base import CommandRule

from messenger_services.messenger_service import MessengerAdapter, MessageHandlerParameters, Message, User


class VkBottleAdapter(MessengerAdapter[VkMessage]):
    def __init__(self, bot: Bot) -> None:
        self.__bot = bot
        self.__api = self.__bot.api

    async def send_message(self, user: User, text: str) -> None:
        await self.__api.messages.send(user.chat_id, message=text, random_id=0)

    def map_message(self, message: VkMessage) -> Message:
        user = self.__map_user(message)
        return Message(user, message.text)

    def __map_user(self, message: VkMessage) -> User:
        return User(message.peer_id)

    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[VkMessage], Awaitable[None]]) -> None:
        self.__bot.on.message(CommandRule(parameters.command, prefixes=['/', '']))(method)
