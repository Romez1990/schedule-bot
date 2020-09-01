from aiogram.types import Message

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

username = ''
user_group = ''


class Subscription:

    async def subscribe(self, message: Message) -> None:
        """
        This handler will be called when user sends '/подписаться [Название_Группы]
        :return: None
        """
        print(message.from_user.username)
        print(message.text)
