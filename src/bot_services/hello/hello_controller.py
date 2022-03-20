from random import choice
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from messenger_services.messenger_service import (
    MessengerController,
    Message,
    controller,
    message_handler,
)


@controller
class HelloController(MessengerController):
    @message_handler('start')
    async def start(self, message: Message) -> None:
        keyboard = ReplyKeyboardMarkup()
        add_group = KeyboardButton('Добавить группу')
        add_group_2 = KeyboardButton('Выбере курс')
        keyboard.add(choice([add_group, add_group_2]))
        await self._send_message(message.user, 'Welcome to the <b>world</b> of schedule', keyboard)

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.user, 'Sorry, I have not been taught to help yet')
