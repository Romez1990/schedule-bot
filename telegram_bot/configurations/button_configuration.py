from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_start = KeyboardButton('/start')
button_help = KeyboardButton('/help')

buttons = ReplyKeyboardMarkup()
buttons.add(button_start, button_help)