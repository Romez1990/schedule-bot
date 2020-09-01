from aiogram import Dispatcher

from .greeting import Greeting
from .subscription import Subscription

from .greeting import Greeting
from .subscription import Subscription


class TelegramDispatcher:
    def __init__(self, subscription: Subscription, greeting: Greeting):
        self.dispatcher = Dispatcher()
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)

