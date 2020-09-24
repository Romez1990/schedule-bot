from asyncio import get_event_loop, AbstractEventLoop

from .env import (
    BaseEnvironment,
    Environment,
)
from .schedule import (
    GroupParser,
    WeekDayTranslator,
)
from .database import (
    Database,
)
from .repositories import (
    UserRepository,
    UserSettingsRepository,
    SubscriptionRepository,
)
from .bot_services import (
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
    env = Environment(base_env)
    group_parser = GroupParser()
    week_day_translator = WeekDayTranslator()
    database = Database(env)
    user_repository = UserRepository(database)
    user_settings_repository = UserSettingsRepository(database)
    subscription_repository = SubscriptionRepository(database)
    subscription_service = SubscriptionService(subscription_repository)
    setting_service = SettingService(user_settings_repository)
    user_service = UserService(user_repository)
    telegram_bot = TelegramBot()
    subscription = Subscription(telegram_bot.bot, subscription_service)
    greeting = Greeting(telegram_bot.bot, user_service)
    theme_decoration = ThemeDecoration(telegram_bot.bot, setting_service)
    telegram_dispatcher = TelegramDispatcher(telegram_bot.bot, subscription, greeting, theme_decoration)
    telegram = Telegram(telegram_dispatcher)

    env.read()
    await database.connect()
    telegram.start()


loop = get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
