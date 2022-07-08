from typing import (
    Callable,
    Awaitable,
)
from vkbottle.bot import (
    Bot,
    Message as VkMessage,
)
from vkbottle.dispatch.rules.base import CommandRule

from messenger_services.messenger_service import (
    MessengerAdapter,
    Message,
    User,
    KeyboardBase,
    MessageHandlerParams,
)


class VkAdapter(MessengerAdapter):
    def __init__(self, bot: Bot) -> None:
        self.__bot = bot
        self.__api = self.__bot.api

    async def send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> None:
        await self.__api.messages.send(user.chat_id, message=text, random_id=0)

    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None:
        rule = CommandRule(params.command, prefixes=['/', ''])
        messenger_handler = self.__map_message_handler(handler)
        self.__bot.on.message(rule)(messenger_handler)

    def __map_message_handler(self, handler: Callable[[Message], Awaitable[None]]
                              ) -> Callable[[VkMessage], Awaitable[None]]:
        async def messenger_handler(messenger_message: VkMessage) -> None:
            message = self.__map_message(messenger_message)
            await handler(message)

        return messenger_handler

    def __map_message(self, message: VkMessage) -> Message:
        user = self.__map_user(message)
        return Message(user, message.text)

    def __map_user(self, message: VkMessage) -> User:
        return User(message.peer_id)
