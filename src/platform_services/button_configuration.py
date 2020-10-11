from aiogram.types import (
    # ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    # InlineKeyboardMarkup,
    # InlineKeyboardButton,
)

from vkwave.bots import (
    Keyboard,
    ButtonColor
)


class ButtonConfiguration:
    def vk_buttons(self) -> Keyboard:
        MENU_VK = Keyboard()
        MENU_VK.add_text_button(text='/start', payload={"command": "start"})
        MENU_VK.add_text_button(text='/help', payload={"command": "help"})
        return MENU_VK

    def telegram_buttons(self) -> ReplyKeyboardMarkup:
        button_start = KeyboardButton('/start')
        button_help = KeyboardButton('/help')

        buttons = ReplyKeyboardMarkup()
        buttons.add(button_start, button_help)
        return buttons


# telegram bot
# button_start = KeyboardButton('/start')
# button_help = KeyboardButton('/help')
#
# buttons = ReplyKeyboardMarkup()
# buttons.add(button_start, button_help)

"""
Here I will take the ReplyKeyboardMarkup button and import them into other .py files.

Тут кнопки будут, их буду брать и портировать в другие файлы .py что бы не захломалять там переменными, тут все кнопки
будут лежать в одном месте
"""
