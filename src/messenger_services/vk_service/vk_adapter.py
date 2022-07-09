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
    Callback,
    Chat,
    KeyboardBase,
    MessageHandlerParams,
    CallbackHandlerParams,
)


class VkAdapter(MessengerAdapter):
    def __init__(self, bot: Bot) -> None:
        self.__bot = bot
        self.__api = self.__bot.api

    async def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> None:
        await self.__api.messages.send(chat.id, message=text, random_id=0)

    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None:
        rule = CommandRule(params.command, prefixes=['/', ''])
        messenger_handler = self.__map_message_handler(handler)
        self.__bot.on.message(rule)(messenger_handler)

    def register_callback_handler(self, params: CallbackHandlerParams,
                                  handler: Callable[[Callback], Awaitable[None]]) -> None:
        ...

    def __map_message_handler(self, handler: Callable[[Message], Awaitable[None]]
                              ) -> Callable[[VkMessage], Awaitable[None]]:
        async def messenger_handler(messenger_message: VkMessage) -> None:
            message = self.__map_message(messenger_message)
            await handler(message)

        return messenger_handler

    def __map_message(self, message: VkMessage) -> Message:
        chat = self.__map_chat(message)
        return Message(chat, message.text)

    def __map_chat(self, message: VkMessage) -> Chat:
        return Chat(message.peer_id)
