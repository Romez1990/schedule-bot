from asyncio import get_event_loop, AbstractEventLoop

from .env import (
    BaseEnvironment,
)
from .database import (
    Database,
)
from .repositories import (
    UserRepository,
    UserSubscribe,
    UserSettings,
)
from .services import (
    UserService,
    SubscriptionService,
    SettingService,
)
from .telegram_bot import (
    Telegram,
    TelegramBot,
    TelegramDispatcher,
    Greeting,
    ThemeDecoration,
    Subscription,
)


async def main(loop: AbstractEventLoop) -> None:
    """
    This function for init then we transfer it to main.py in root directory
    :return: None
    """
    base_env = BaseEnvironment()
    database = Database()
    user_repository = UserRepository(database)
    user_settings = UserSettings(database)
    user_subscribe = UserSubscribe(database)
    subscription_service = SubscriptionService(user_subscribe)
    setting_service = SettingService(user_settings)
    user_service = UserService(user_repository)
    telegram_bot = TelegramBot()
    subscription = Subscription(telegram_bot.bot, subscription_service)
    greeting = Greeting(telegram_bot.bot, user_service)
    theme_decoration = ThemeDecoration(telegram_bot.bot, setting_service)
    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting, theme_decoration)
    telegram = Telegram(telegram_dispatcher)

    await database.connect()
    telegram.start()


loop = get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
