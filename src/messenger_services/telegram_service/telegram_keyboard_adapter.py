from typing import (
    Sequence,
    TypeAlias,
)
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

from infrastructure.ioc_container import service
from data.vector import List
from messenger_services.messenger_service import (
    KeyboardBase,
    Keyboard,
    InlineKeyboard,
    ButtonBase,
    Button,
    InlineButton,
    PayloadSerializer,
)

TelegramKeyboard: TypeAlias = ReplyKeyboardMarkup | InlineKeyboardMarkup
TelegramButton: TypeAlias = KeyboardButton | InlineKeyboardButton


@service(to_self=True)
class TelegramKeyboardAdapter:
    def __init__(self, payload_serializer: PayloadSerializer) -> None:
        self.__payload_serializer = payload_serializer

    def map_keyboard(self, keyboard: KeyboardBase) -> TelegramKeyboard:
        messenger_keyboard = self.__create_keyboard(keyboard)
        rows = List(keyboard.buttons) \
            .map(self.__map_row)
        for row in rows:
            messenger_keyboard.row(*row)
        return messenger_keyboard

    def __create_keyboard(self, keyboard: KeyboardBase) -> TelegramKeyboard:
        match keyboard:
            case Keyboard(resize=resize):
                return ReplyKeyboardMarkup(resize_keyboard=resize)
            case InlineKeyboard():
                return InlineKeyboardMarkup()
            case _:
                raise RuntimeError

    def __map_row(self, row: Sequence[ButtonBase]) -> Sequence[TelegramButton]:
        return List(row) \
            .map(self.__map_button)

    def __map_button(self, button: ButtonBase) -> TelegramButton:
        args_base = [button.text]
        match button:
            case Button():
                return KeyboardButton(*args_base)
            case InlineButton(payload=payload):
                data = self.__payload_serializer.serialize(payload)
                return InlineKeyboardButton(*args_base, callback_data=data)
            case _:
                raise RuntimeError
