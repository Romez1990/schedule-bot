from aiogram import Bot
from aiogram.types import Message

import logging

# Configure logging
from src.telegram_bot.telegram_bot import TelegramBot

logging.basicConfig(level=logging.INFO)


class Subscription:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def subscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """

        username = message.from_user.username
        group_input_from_user = message.text
        user_group = group_input_from_user.split()

        if len(username) > 1 and len(user_group[1]) > 6:
            await self.bot.send_message(message.from_user.id,
                                        f'Ваше имя: "{username}" и группа "{user_group[1]}" '
                                        f'успешна добавлена в база данных')
        elif len(username) < 1 and len(username) < 6:
            await self.bot.send_message(message.from_user.id, 'У вас недействительные данные')

        else:
            await self.bot.send_message(message.from_user.id, 'Произошла ошибка')