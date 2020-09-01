from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting

from .telegram_bot.telegram import Telegram
from .telegram_bot.telegram_dispatcher import TelegramDispatcher


def main():
    telegram_bot = TelegramBot()
    subscription = Subscription(telegram_bot.bot)
    greeting = Greeting()

    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting)
    telegram = Telegram(telegram_dispatcher)
    telegram.start()
