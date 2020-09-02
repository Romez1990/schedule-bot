from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting

from .telegram_bot.telegram import Telegram
from .telegram_bot.telegram_dispatcher import TelegramDispatcher


def main() -> None:
    """
    This function for init then we transfer it to main.py in root directory
    :return: None
    """
    telegram_bot = TelegramBot()
    subscription = Subscription(telegram_bot.bot)
    greeting = Greeting()

    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting)
    telegram = Telegram(telegram_dispatcher)
    telegram.start()
