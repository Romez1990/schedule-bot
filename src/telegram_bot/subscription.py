from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ParseMode

from .configurations.messages_text import message_subscribe


class Subscription:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def subscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """
        user_group = [mess.upper() for mess in message.text.split()][1]

        if len(user_group) > 6:
            await self.bot.send_message(message.from_user.id, message_subscribe(user_group, True),
                                        parse_mode=ParseMode.HTML)
        elif len(user_group) < 6:
            await self.bot.send_message(message.from_user.id, 'У вас недействительные данные')

        else:
            await self.bot.send_message(message.from_user.id, 'Произошла ошибка')

    async def unsubscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/отписаться [Название_Группы]
        :return: None
        """

        user_group = [mess.upper() for mess in message.text.split()][1]

        if len(user_group) > 6:
            await self.bot.send_message(message.from_user.id, message_subscribe(user_group, False),
                                        parse_mode=ParseMode.HTML)

        elif len(user_group) < 6:
            await self.bot.send_message(message.from_user.id, f'У вас недействительные данные')

        else:
            await self.bot.send_message(message.from_user.id, f'Извините, произошла ошибка')
