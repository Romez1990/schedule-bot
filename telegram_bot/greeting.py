from aiogram import executor, types
from telegram_bot.configurations.configure import dp
from telegram_bot.configurations.button_configuration import buttons
from aiogram.types import ParseMode

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
        message_text = '''
<strong>Приветствую дорогой студент👋<strike>или уже не студент</strike>\n
🦾Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻\n
Напиши мне: подписаться [Название_Группы] (без квадратной скобки)</strong>
        '''
        await message.reply(message_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

    @dp.message_handler(commands=['help'])
    async def send_help(message: types.Message) -> None:
        """
        This handler will be called when user sends `/help`
        :param message: types.Message
        :return: None
        """
        message_text = '''
<em>/start</em> - <strong>команда для старта бота</strong> (по умолчанию включен)\n
<em>Подписаться [Название_Группы]</em> - <strong>подписаться на рассылку расписание</strong>\n
<em>Отписаться [Название_Группы]</em> - <strong>отписаться от рассылки расписание</strong>\n
<em>Тёмная тема</em> - <strong>получаться рассылку расписание в тёмной теме</strong>\n
<em>Светлая тема</em> - <strong>получаться рассылку расписание в светвлой теме</strong>\n
        '''

        await message.reply(message_text, reply_markup=buttons, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
