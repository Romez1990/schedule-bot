from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ParseMode

from .configurations.messages_text import message_subscribe
from ..services.subscription_service import SubscriptionService


class Subscription:
    def __init__(self, bot: Bot, user_subscription: SubscriptionService):
        self.bot = bot
        self.user_subscription = user_subscription

    async def subscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """
        user_group = [mess.upper() for mess in message.text.split()][1]

        if len(user_group) > 6:
            await self.bot.send_message(message.from_user.id, message_subscribe(user_group, True),
                                        parse_mode=ParseMode.HTML)
            await self.user_subscription.add(user_id=0, group_name=user_group)  # here need worked user_id
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
            await self.user_subscription.delete(user_id=0, group_name=user_group)  # here need worker_user_id

        elif len(user_group) < 6:
            await self.bot.send_message(message.from_user.id, f'У вас недействительные данные')

        else:
            await self.bot.send_message(message.from_user.id, f'Извините, произошла ошибка')

    async def change(self, message: Message) -> None:
        user_group = [mess.upper() for mess in message.text.split()][1]
        if len(user_group) > 6:
            await self.user_subscription.change(1, user_group)
            await self.bot.send_message(message.from_user.id, f'Данные успешно изменены')
