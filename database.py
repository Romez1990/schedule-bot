from asyncio import run

from src.database import Database
from src.repositories import UserRepository


async def main():
    database = Database()
    await database.connect()
    user_repository = UserRepository(database)
    await user_repository.add('telegram', '228')
    await user_repository.delete('telegram', '228')


run(main())