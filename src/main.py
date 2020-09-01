from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting

from .telegram_bot.telegram import Telegram
from .telegram_bot.telegram_dispatcher import TelegramDispatcher


def main():
    subscription = Subscription()
    greeting = Greeting()
    telegram_bot = TelegramBot(subscription, greeting)
    # telegram_bot.start()
    dispatcher = TelegramDispatcher(telegram_bot, subscription, greeting)
    telegram = Telegram()
    telegram
