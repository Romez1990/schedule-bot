from aiogram import Bot
from aiogram.types import Message


import logging

# Configure logging
from src.telegram_bot.telegram_bot import TelegramBot

logging.basicConfig(level=logging.INFO)

username = ''
user_group = ''


class Subscription:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def subscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """
        print(message.from_user.username)
        print(message.text)

        if len(message.from_user.username) and len(message.text) > 5:
            await self.bot.send_message(message.from_user.id,
                f'Ваше имя: {message.from_user.username} и группа {message.text} успешна добавлена в база данных')
        else:
            await self.bot.send_message('Error')