from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from vkwave.bots import (
    Keyboard,
)


class ButtonConfiguration:
    def __init__(self) -> None:
        self.MENU_VK = Keyboard()
        self.TELEGRAM_MENU = ReplyKeyboardMarkup()

    def vk_buttons(self) -> Keyboard:
        self.MENU_VK.add_text_button(text='/start', payload={"command": "start"})
        self.MENU_VK.add_text_button(text='/help', payload={"command": "help"})
        return self.MENU_VK

    def telegram_buttons(self) -> ReplyKeyboardMarkup:
        BUTTON_START = KeyboardButton('/start')
        BUTTON_HELP = KeyboardButton('/help')
        self.TELEGRAM_MENU.add(BUTTON_START, BUTTON_HELP)
        return self.TELEGRAM_MENU
