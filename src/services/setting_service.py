from ..repositories import UserSettings


class SettingService:
    def __init__(self, user_settings: UserSettings):
        self.user_settings = user_settings

    async def add(self, user_id, theme):
        await self.user_settings.add(user_id, theme)

    async def delete(self, user_id, theme):
        await self.user_settings.delete(user_id, theme)
