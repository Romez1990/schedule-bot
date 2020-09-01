from aiogram import Dispatcher


from .greeting import Greeting
from .subscription import Subscription
from .telegram_bot import TelegramBot


class TelegramDispatcher:
    def __init__(self, bot: TelegramBot,subscription: Subscription, greeting: Greeting):
        self.dispatcher = Dispatcher(bot.bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)

