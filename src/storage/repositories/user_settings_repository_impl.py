from data.fp.task import taskify
from data.vector import List
from storage.entities import (
    User,
    UserSettings,
)
from storage.database import (
    Record,
)
from .repository_base import RepositoryBase
from .user_settings_repository import UserSettingsRepository


class UserSettingsRepositoryImpl(UserSettingsRepository, RepositoryBase):
    @taskify
    async def save(self, user_settings: UserSettings) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO user_settings(user_id, name, value)
                VALUES ($1, $2, $3)
            ''', user_settings.user.id, user_settings.name, user_settings.value)

    async def delete(self, user_settings: UserSettings) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                DELETE FROM user_settings WHERE id = $1
            ''', user_settings.id)

    async def find_all(self, user: User) -> List[UserSettings]:
        async with self._get_connection() as connection:
            user_settings = await connection.fetch('''
                SELECT * FROM user_settings
                WHERE user_id = $1
            ''', user.id)
            return List(user_settings) \
                .map(self.__create_user_settings)

    def __create_user_settings(self, record: Record) -> UserSettings:
        return UserSettings(**record)
