from src.database import UserSettingsRepositoryInterface
from src.entities import User, UserSettings
from .user_settings_service_interface import UserSettingsServiceInterface


class UserSettingsService(UserSettingsServiceInterface):
    def __init__(self, user_settings: UserSettingsRepositoryInterface) -> None:
        self.__user_settings = user_settings

    async def create_default_settings(self, user: User) -> UserSettings:
        default_theme = 'light'
        user_settings = UserSettings(user, default_theme)
        await self.__user_settings.save(user_settings)
        return user_settings

    async def find(self, user: User) -> UserSettings:
        return await self.__user_settings.find_by_user(user)
