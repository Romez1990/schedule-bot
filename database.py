from asyncio import run

from src.database import Database
from src.repositories import UserRepository
from src.repositories import UserSettings
from src.repositories import UserSubscribe

from src.database.config import database_config as dc


def users():
    pass


def subscriptions():
    pass


def user_settings():
    pass


async def main():
    database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
    await database.connect()
    user_repository = UserRepository(database)
    user_settings = UserSettings(database)
    user_subscriptions = UserSubscribe(database)
    await user_repository.add('VK', '22822222')
    # await user_repository.delete('telegram', '228')
    # await user_settings.add(1, 'Тёмная')
    # await user_subscriptions.add(1, 'ЗВТ-18-9222')


run(main())
