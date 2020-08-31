from aiogram import executor, types
from aiogram.types import ParseMode

from telegram_bot.configurations.configure import dp
from telegram_bot.configurations.messages_text import message_text_start, message_text_help
from telegram_bot.configurations.button_configuration import buttons

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

username = ''
user_group = ''


class Subscription:
    def __init__(self):
        pass

    @dp.message_handler(commands=['подписаться'])
    async def subscribe(message: types.Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
