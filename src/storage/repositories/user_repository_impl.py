from infrastructure.ioc_container import service
from storage.database import Record
from storage.entities import User
from data.fp.maybe import Maybe
from data.fp.task import taskify
from data.fp.task_maybe import task_maybeify
from .user_repository import UserRepository
from .repository_base import RepositoryBase


@service
class UserRepositoryImpl(UserRepository, RepositoryBase):
    @taskify
    async def save(self, user: User) -> User:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO users(messenger, messenger_id)
                VALUES ($1, $2)
            ''', user.messenger, user.messenger_id)
            user_id = await connection.fetch_value('''SELECT currval('users_id_seq')''', value_type=int)
            return user.set_id(user_id)

    @task_maybeify
    async def find(self, messenger: str, messenger_id: str) -> Maybe[User]:
        async with self._get_connection() as connection:
            return await connection.fetch_row('''
                SELECT * FROM users
                WHERE messenger = $1 AND messenger_id = $2
            ''', messenger, messenger_id) \
                .map(self.__create_maybe_user)

    def __create_maybe_user(self, maybe_record: Maybe[Record]) -> Maybe[User]:
        return maybe_record.map(self.__create_user)

    def __create_user(self, record: Record) -> User:
        return User(**record)
