from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting
from .telegram_bot.theme_decoration import ThemeDecoration

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
    theme_decoration = ThemeDecoration(telegram_bot.bot)

    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting, theme_decoration)
    telegram = Telegram(telegram_dispatcher)
    telegram.start()
