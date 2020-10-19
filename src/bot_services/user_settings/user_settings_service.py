from src.database import UserSettingsRepositoryInterface
from src.entities import User, UserSettings
from src.schedule_services import (
    ThemeRepositoryInterface,
)
from .user_settings_service_interface import UserSettingsServiceInterface


class UserSettingsService(UserSettingsServiceInterface):
    def __init__(self, user_settings: UserSettingsRepositoryInterface, themes: ThemeRepositoryInterface) -> None:
        self.__user_settings = user_settings
        self.__themes = themes

    async def create_default_settings(self, user: User) -> UserSettings:
        default_theme = self.__themes.get_by_name('light').unwrap()
        user_settings = UserSettings(user, default_theme)
        await self.__user_settings.save(user_settings)
        return user_settings

    async def find(self, user: User) -> UserSettings:
        return await self.__user_settings.find_by_user(user)
