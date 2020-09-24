from ..repositories import UserSettingsRepository


class SettingService:
    def __init__(self, user_settings: UserSettingsRepository):
        self.user_settings = user_settings

    async def add(self, user_id: int, theme: str) -> None:
        await self.user_settings.add(user_id, theme)

    async def delete(self, user_id: int, theme: str) -> None:
        await self.user_settings.delete(user_id, theme)

    async def change(self, user_id: int, theme: str) -> None:
        await self.user_settings.change(user_id, theme)
