from src.entities import User, UserSettings


class AbstractUserSettingsRepository:
    async def save(self, user_settings: UserSettings) -> UserSettings:
        raise NotImplementedError

    async def delete(self, user_settings: UserSettings) -> None:
        raise NotImplementedError

    async def update(self, user_settings: UserSettings) -> None:
        raise NotImplementedError

    async def find_by_user(self, user: User) -> UserSettings:
        raise NotImplementedError
