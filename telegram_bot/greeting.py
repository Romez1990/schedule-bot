from aiogram import executor
from aiogram.types import Message
from aiogram.types import ParseMode

from telegram_bot.configurations.configure import dp
from telegram_bot.configurations.messages_text import message_text_start, message_text_help
from telegram_bot.configurations.button_configuration import buttons

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class Greeting:
    def __init__(self):
        pass

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: Message) -> None:
        """
        This handler will be called when user sends `/start`
        :param message: types.Message
        :return: None
        """
        # message_text_start are taken from directory configurations/messages_text.py
        # buttons are taken from directory configurations/buttons.py
        await message.reply(message_text_start, reply_markup=buttons, parse_mode=ParseMode.HTML)

    @dp.message_handler(commands=['help'])
    async def send_help(message: Message) -> None:
        """
        This handler will be called when user sends `/help`
        :param message: types.Message
        :return: None
        """
        # message_text_start are taken from directory configurations/messages_text.py
        # buttons are taken from directory configurations/buttons.py
        await message.reply(message_text_help, reply_markup=buttons, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
