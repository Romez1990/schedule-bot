from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from vkwave.bots import (
    Keyboard,
)


class ButtonConfiguration:

    def vk_buttons(self):
        MENU_VK = Keyboard()
        MENU_VK.add_text_button(text='/start')
        MENU_VK.add_text_button(text='/help')
        return MENU_VK

    def telegram_buttons(self) -> ReplyKeyboardMarkup:
        TELEGRAM_MENU = ReplyKeyboardMarkup()
        BUTTON_START = KeyboardButton('/start')
        BUTTON_HELP = KeyboardButton('/help')
        TELEGRAM_MENU.add(BUTTON_START, BUTTON_HELP)
        return TELEGRAM_MENU
