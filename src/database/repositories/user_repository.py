from returns.maybe import Maybe

from src.entities import User
from ..database import Database
from .abstract_user_repository import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, database: Database):
        self.__database = database

    async def save(self, user: User) -> User:
        await self.__database.execute('''
            INSERT INTO users(platform, platform_id)
            VALUES ($1, $2)
        ''', user.platform, user.platform_id)
        id = await self.__database.fetch_value('''
            SELECT currval('users_id_seq')
        ''')
        return User(user.platform, user.platform_id, id)

    async def find(self, platform: str, platform_id: str) -> Maybe[User]:
        return (await self.__database.fetch_row('''
            SELECT * FROM users
            WHERE platform = $1 AND platform_id = $2
        ''', platform, platform_id)) \
            .map(lambda user_record: User(**user_record))
