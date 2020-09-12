from asyncio import get_event_loop

from .database import Database
from .repositories import UserRepository
from .services.user_service import UserService
from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting
from .telegram_bot.theme_decoration import ThemeDecoration

from .telegram_bot.telegram import Telegram
from .telegram_bot.telegram_dispatcher import TelegramDispatcher


async def async_main() -> None:
    """
    This function for init then we transfer it to main.py in root directory
    :return: None
    """
    telegram_bot = TelegramBot()
    database = Database()
    await database.connect()
    user_repository = UserRepository(database)
    user_service = UserService(user_repository)
    subscription = Subscription(telegram_bot.bot)
    greeting = Greeting(telegram_bot.bot, user_service)
    theme_decoration = ThemeDecoration(telegram_bot.bot)

    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting, theme_decoration)
    telegram = Telegram(telegram_dispatcher)
    telegram.start()


def main():
    loop = get_event_loop()
    loop.create_task(async_main())
    loop.run_forever()