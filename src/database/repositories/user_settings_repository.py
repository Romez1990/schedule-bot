from src.entities import UserSettings, User
from src.schedule_services import (
    ThemeRepositoryInterface,
)
from ..database import Database
from .user_settings_repository_interface import UserSettingsRepositoryInterface


class UserSettingsRepository(UserSettingsRepositoryInterface):
    def __init__(self, database: Database, themes: ThemeRepositoryInterface) -> None:
        self.__database = database
        self.__themes = themes

    async def save(self, user_settings: UserSettings) -> UserSettings:
        await self.__database.execute('''
            INSERT INTO user_settings(user_id, theme)
            VALUES ($1, $2)
        ''', user_settings.user.id, user_settings.theme.name)
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
        ''', user_settings.user.id, user_settings.theme.name)

    async def find_by_user(self, user: User) -> UserSettings:
        maybe_user_settings_record = await self.__database.fetch_row('''
            SELECT theme FROM user_settings
            WHERE user_id = $1
        ''', user.id)
        user_settings_record = maybe_user_settings_record.unwrap()
        theme = self.__themes.get_by_name(user_settings_record.pop('theme')).unwrap()
        return UserSettings(user, theme)
