from aiogram.types import (
    # ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    # InlineKeyboardMarkup,
    # InlineKeyboardButton,
)

button_start = KeyboardButton('/start')
button_help = KeyboardButton('/help')

buttons = ReplyKeyboardMarkup()
buttons.add(button_start, button_help)

"""
Here I will take the ReplyKeyboardMarkup button and import them into other .py files.

Тут кнопки будут, их буду брать и портировать в другие файлы .py что бы не захломалять там переменными, тут все кнопки
будут лежать в одном месте
"""
