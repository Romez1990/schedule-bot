from asyncio import get_event_loop

from .database import Database
from .repositories import UserRepository
from .repositories import UserSubscribe
from .repositories import UserSettings

from .services.user_service import UserService
from .services.subscription_service import SubscriptionService
from .services.setting_service import SettingService

from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting
from .telegram_bot.theme_decoration import ThemeDecoration

from .telegram_bot.telegram import Telegram
from .telegram_bot.telegram_dispatcher import TelegramDispatcher


async def main() -> None:
    """
    This function for init then we transfer it to main.py in root directory
    :return: None
    """
    telegram_bot = TelegramBot()
    database = Database()
    await database.connect()

    user_repository = UserRepository(database)
    user_settings = UserSettings(database)
    user_subscribe = UserSubscribe(database)

    subscription_service = SubscriptionService(user_subscribe)
    setting_service = SettingService(user_settings)
    user_service = UserService(user_repository)

    subscription = Subscription(telegram_bot.bot, subscription_service)
    greeting = Greeting(telegram_bot.bot, user_service)
    theme_decoration = ThemeDecoration(telegram_bot.bot, setting_service)

    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting, theme_decoration)
    telegram = Telegram(telegram_dispatcher)
    telegram.start()


loop = get_event_loop()
loop.create_task(main())
loop.run_forever()
