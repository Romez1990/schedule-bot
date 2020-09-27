from asyncio import get_event_loop, AbstractEventLoop

from src.env import (
    BaseEnvironment,
    Environment,
)
from src.schedule import (
    GroupParser,
    WeekDayTranslator,
)
from src.database import (
    Database,
)
from src.repositories import (
    UserRepository,
    UserSettingsRepository,
    SubscriptionRepository,
)
from src.bot_services import (
    UserService,
    UserSettingsService,
    SubscriptionService,
)
from src.telegram_service import (
    TelegramService,
    TelegramBot,
    TelegramController,
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
    user_settings_service = UserSettingsService(user_settings_repository)
    subscription_service = SubscriptionService(subscription_repository, group_parser)
    user_service = UserService(user_repository, user_settings_service, subscription_service)
    telegram_bot = TelegramBot(env)
    controller = TelegramController(telegram_bot, user_service, user_settings_service, subscription_service)
    telegram_service = TelegramService(telegram_bot, controller)

    env.read()
    await database.connect()
    loop.create_task(telegram_service.start())


loop = get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
