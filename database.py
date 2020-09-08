from asyncio import run

from src.database import Database
from src.repositories import UserRepository
from src.repositories import UserSettings


async def main():
    database = Database()
    await database.connect()
    user_repository = UserRepository(database)
    user_settings = UserSettings(database)
    # await user_repository.add('telegram', '228')
    # await user_repository.delete('telegram', '228')
    await user_settings.add(1, 'Тёмная')


run(main())