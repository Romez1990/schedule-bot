from typing import (
    Callable,
    Awaitable,
)
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import (
    Command,
    Text,
)
from aiogram.types import (
    Message as TelegramMessage,
    Chat as TelegramChat,
)

from data.fp.maybe import Maybe
from messenger_services.messenger_service import (
    MessengerAdapter,
    Chat,
    Message,
    KeyboardBase,
    MessageHandlerParams,
)
from .telegram_keyboard_adapter import TelegramKeyboardAdapter


class TelegramAdapter(MessengerAdapter):
    def __init__(self, bot: Bot, dispatcher: Dispatcher, keyboard_adapter: TelegramKeyboardAdapter) -> None:
        self.__bot = bot
        self.__dispatcher = dispatcher
        self.__keyboard_adapter = keyboard_adapter

    async def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> None:
        messenger_keyboard = Maybe.from_optional(keyboard) \
            .map(self.__keyboard_adapter.map_keyboard) \
            .get_or_none()
        await self.__bot.send_message(chat.id, text, reply_markup=messenger_keyboard)

    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None:
        filters = Command(params.command) | Text(params.command)
        messenger_handler = self.__map_message_handler(handler)
        self.__dispatcher.message_handler(filters)(messenger_handler)

    def __map_message_handler(self, handler: Callable[[Message], Awaitable[None]]
                              ) -> Callable[[TelegramMessage], Awaitable[None]]:
        async def messenger_handler(messenger_message: TelegramMessage) -> None:
            message = self.__map_message(messenger_message)
            await handler(message)

        return messenger_handler

    def __map_message(self, message: TelegramMessage) -> Message:
        chat = self.__map_chat(message.chat)
        return Message(chat, message.text)

    def __map_chat(self, chat: TelegramChat) -> Chat:
        return Chat(chat.id)
