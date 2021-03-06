from src.entities import User, UserSettings


class UserSettingsServiceInterface:
    async def create_default_settings(self, user: User) -> UserSettings:
        raise NotImplementedError

    async def find(self, user: User) -> UserSettings:
        raise NotImplementedError
