from typing import (
    Sequence,
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
    Chat,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

from data.fp.maybe import Maybe
from data.vector import List
from messenger_services.messenger_service import (
    MessengerAdapter,
    User,
    Message,
    KeyboardBase,
    Keyboard,
    InlineKeyboard,
    ButtonBase,
    Button,
    InlineButton,
    MessageHandlerParams,
)


class TelegramAdapter(MessengerAdapter):
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self.__bot = bot
        self.__dispatcher = dispatcher

    async def send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> None:
        messenger_keyboard = Maybe.from_optional(keyboard) \
            .map(self.__map_keyboard) \
            .get_or_none()
        await self.__bot.send_message(user.chat_id, text, reply_markup=messenger_keyboard)

    def __map_keyboard(self, keyboard: KeyboardBase) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
        messenger_keyboard = self.__create_keyboard(keyboard)
        rows = List(keyboard.buttons) \
            .map(self.__map_row)
        for row in rows:
            messenger_keyboard.row(*row)
        return messenger_keyboard

    def __create_keyboard(self, keyboard: KeyboardBase) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
        match keyboard:
            case Keyboard(resize=resize):
                return ReplyKeyboardMarkup(resize_keyboard=resize)
            case InlineKeyboard():
                return InlineKeyboardMarkup()
            case _:
                raise RuntimeError

    def __map_row(self, buttons: Sequence[ButtonBase]) -> Sequence[KeyboardButton | InlineKeyboardButton]:
        return List(buttons) \
            .map(self.__map_button)

    def __map_button(self, button: ButtonBase) -> KeyboardButton | InlineKeyboardButton:
        args_base = [button.text]
        match button:
            case Button():
                return KeyboardButton(*args_base)
            case InlineButton(payload):
                return InlineKeyboardButton(*args_base, callback_data=payload)
            case _:
                raise RuntimeError

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
        user = self.__map_user(message.chat)
        return Message(user, message.text)

    def __map_user(self, chat: Chat) -> User:
        return User(chat.id)
