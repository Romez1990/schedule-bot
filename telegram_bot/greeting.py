from aiogram import Bot, Dispatcher, executor, types
from asyncio import run

import asyncio
import logging
import os

API_TOKEN = os.getenv('API_KEY_SCHEDULE_BOT')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class Greeting:
    def __init__(self):
        pass

    @dp.message_handler(commands=['start'])
    async def send_welcome(self, message: types.Message) -> None:
        """
        This handler will be called when user sends `/start`
        :param message: types.Message
        :return: None
        """
        await message.reply('Привет я бот')

    @dp.message_handler(commands=['/help'])
    async def send_help(self, message: types.Message) -> None:
        """
        This handler will be called when user sends `/help`
        :param message: types.Message
        :return: None
        """

        await message.reply('Тут помощь :3')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
