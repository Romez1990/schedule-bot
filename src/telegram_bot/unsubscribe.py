from aiogram import Bot
from aiogram.types import Message


class Unsubscribe:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def unsubscribe(self, message: Message) -> None:
        """
        This method will be called when user write `/отписаться [Название_группы
        :param message:
        :return: None
        """

        username = message.from_user.username
        group_input_from_user = message.text

        user_group = group_input_from_user.split()
        
        if len(username) > 1 and len(user_group[1]) > 6:
            await self.bot.send_message(message.from_user.id,
                                        f'{username} успешно отписался от рассылки на группу {user_group[1]}')

        elif len(username) < 1 and len(user_group[1]) < 6:
            await self.bot.send_message(message.from_user.id, f'У вас недействительные данные')

        else:
            await self.bot.send_message(message.from_user.id, f'Извините, произошла ошибка')
