from aiogram import executor, types
from telegram_bot.configurations.configure import dp
from telegram_bot.configurations.button_configuration import buttons

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class Greeting:
    def __init__(self):
        pass

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message) -> None:
        """
        This handler will be called when user sends `/start`
        :param message: types.Message
        :return: None
        """
        await message.reply('Привет я бот', reply_markup=buttons)

    @dp.message_handler(commands=['help'])
    async def send_help(message: types.Message) -> None:
        """
        This handler will be called when user sends `/help`
        :param message: types.Message
        :return: None
        """
        await message.reply('Тут помощь :3', reply_markup=buttons)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
