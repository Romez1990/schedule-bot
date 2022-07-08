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
    Payload,
)

TelegramKeyboard: TypeAlias = ReplyKeyboardMarkup | InlineKeyboardMarkup
TelegramButton: TypeAlias = KeyboardButton | InlineKeyboardButton


@service(to_self=True)
class TelegramKeyboardAdapter:
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

    def __map_row(self, buttons: Sequence[ButtonBase]) -> Sequence[TelegramButton]:
        return List(buttons) \
            .map(self.__map_button)

    def __map_button(self, button: ButtonBase) -> TelegramButton:
        args_base = [button.text]
        match button:
            case Button():
                return KeyboardButton(*args_base)
            case InlineButton(payload=payload):
                return InlineKeyboardButton(*args_base, callback_data=self.__serialize_payload(payload))
            case _:
                raise RuntimeError

    def __serialize_payload(self, payload: Payload) -> str:
        import json
        payload_dict = payload.__dict__
        payload_dict['type'] = payload.type
        return json.dumps(payload_dict, ensure_ascii=False)
