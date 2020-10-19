from returns.maybe import Nothing
from returns.future import Future, FutureResult

from src.database import UserSettingsRepositoryInterface
from src.entities import User, UserSettings
from src.schedule_services import (
    ThemeRepositoryInterface,
)
from .errors import (
    ThemeNotFoundError,
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

    def change(self, user: User, theme_name: str) -> FutureResult[None, ThemeNotFoundError]:
        maybe_theme = self.__themes.get_by_name(theme_name)
        if maybe_theme is Nothing:
            return FutureResult.from_failure(ThemeNotFoundError(theme_name))
        theme = maybe_theme.unwrap()
        user_settings = UserSettings(user, theme)

        return FutureResult.from_future(Future.from_io())
