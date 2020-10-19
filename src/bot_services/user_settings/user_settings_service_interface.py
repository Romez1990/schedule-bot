from returns.future import FutureResult

from src.entities import User, UserSettings
from .errors import (
    ThemeNotFoundError,
)


class UserSettingsServiceInterface:
    async def create_default_settings(self, user: User) -> UserSettings:
        raise NotImplementedError

    async def find(self, user: User) -> UserSettings:
        raise NotImplementedError

    def change(self, user: User, theme_name: str) -> FutureResult[None, ThemeNotFoundError]:
        raise NotImplementedError
