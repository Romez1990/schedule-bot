from ..entities import User, UserSettings
from ..repositories import UserSettingsRepository
from .abstract_user_settings_service import AbstractUserSettingsService


class UserSettingsService(AbstractUserSettingsService):
    def __init__(self, user_settings: UserSettingsRepository) -> None:
        self.__user_settings = user_settings

    async def create_default_settings(self, user: User) -> UserSettings:
        default_theme = 'light'
        user_settings = UserSettings(user, default_theme)
        await self.__user_settings.save(user_settings)
        return user_settings

    async def find(self, user: User) -> UserSettings:
        return await self.__user_settings.find_by_user(user)
