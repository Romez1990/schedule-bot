from typing import (
    Sequence,
    MutableMapping,
    TypeAlias,
)
from vkbottle import (
    Keyboard as VkKeyboard,
    Text,
    Callback,
)

from infrastructure.ioc_container import service
from data.vector import List
from messenger_services.messenger_service import (
    PayloadSerializer,
    KeyboardBase,
    Keyboard,
    InlineKeyboard,
    ButtonBase,
    Button,
    InlineButton,
)

VkButton: TypeAlias = Text | Callback


@service(to_self=True)
class VkKeyboardAdapter:
    def __init__(self, payload_serializer: PayloadSerializer) -> None:
        self.__payload_serializer = payload_serializer

    def map_keyboard(self, keyboard: KeyboardBase) -> VkKeyboard:
        messenger_keyboard = self.__create_keyboard(keyboard)
        rows = List(keyboard.buttons) \
            .map(self.__map_row)
        for i, row in enumerate(rows):
            for button in row:
                messenger_keyboard.add(button)
            if i != len(rows) - 1:
                messenger_keyboard.row()
        return messenger_keyboard

    def __create_keyboard(self, keyboard: KeyboardBase) -> VkKeyboard:
        kwargs: MutableMapping[str, object] = {}
        match keyboard:
            case Keyboard():
                pass
            case InlineKeyboard():
                kwargs.update({
                    'inline': True,
                })
            case _:
                raise RuntimeError
        return VkKeyboard(**kwargs)

    def __map_row(self, row: Sequence[ButtonBase]) -> Sequence[VkButton]:
        return List(row) \
            .map(self.__map_button)

    def __map_button(self, button: ButtonBase) -> VkButton:
        args_base = [button.text]
        match button:
            case Button():
                return Text(*args_base)
            case InlineButton(payload=payload):
                data = self.__payload_serializer.serialize(payload)
                return Callback(*args_base, payload=data)
            case _:
                raise RuntimeError
