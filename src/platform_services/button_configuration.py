from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from vkwave.bots import (
    Keyboard,
)


class ButtonConfiguration:
    def vk_buttons(self) -> Keyboard:
        MENU_VK = Keyboard()
        MENU_VK.add_text_button(text='/start', payload={"command": "start"})
        MENU_VK.add_text_button(text='/help', payload={"command": "help"})
        return MENU_VK

    def telegram_buttons(self) -> ReplyKeyboardMarkup:
        BUTTON_START = KeyboardButton('/start')
        BUTTON_HELP = KeyboardButton('/help')

        BUTTONS = ReplyKeyboardMarkup()
        BUTTONS.add(BUTTON_START, BUTTON_HELP)
        return BUTTONS
