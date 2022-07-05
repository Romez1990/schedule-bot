from typing import (
    Callable,
    Awaitable,
)
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import (
    Message as TelegramMessage,
    Chat,
)

from messenger_services.messenger_service import (
    MessengerAdapter,
    User,
    Message,
)
from messenger_services.messenger_service.message_handler_decorator import MessageHandlerParameters


class TelegramAdapter(MessengerAdapter[TelegramMessage]):
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self.__bot = bot
        self.__dispatcher = dispatcher

    async def send_message(self, user: User, text: str) -> None:
        await self.__bot.send_message(user.chat_id, text)

    def map_message(self, message: TelegramMessage) -> Message:
        user = self.__map_user(message.chat)
        return Message(user, message.text)

    def __map_user(self, chat: Chat) -> User:
        return User(chat.id)

    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[TelegramMessage], Awaitable[None]]) -> None:
        self.__dispatcher.message_handler(Command(parameters.command, prefixes=['/', '']))(method)
