from src.entities import UserSettings, User
from ..database import Database
from .abstract_user_settings_repository import AbstractUserSettingsRepository


class UserSettingsRepository(AbstractUserSettingsRepository):
    def __init__(self, database: Database):
        self.__database = database

    async def save(self, user_settings: UserSettings) -> UserSettings:
        await self.__database.execute('''
            INSERT INTO user_settings(user_id, theme)
            VALUES ($1, $2)
        ''', user_settings.user.id, user_settings.theme)
        return user_settings

    async def delete(self, user_settings: UserSettings) -> None:
        await self.__database.execute('''
            DELETE from user_settings
            WHERE user_id = $1
        ''', user_settings.user.id)

    async def update(self, user_settings: UserSettings) -> None:
        await self.__database.execute('''
            UPDATE user_settings
            SET theme = $2
            WHERE user_id = $1 
        ''', user_settings.user.id, user_settings.theme)

    async def find_by_user(self, user: User) -> UserSettings:
        maybe_user_settings_record = await self.__database.fetch_row('''
            SELECT theme FROM user_settings
            WHERE user_id = $1
        ''', user.id)
        return UserSettings(user, **maybe_user_settings_record.unwrap())
