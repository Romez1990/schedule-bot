from asyncio import run

from ..database import Database


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    async def add(self, platform: str, platform_id: str) -> None:
        await self.database.execute('''
            INSERT INTO users(platform, platform_id) VALUES ($1, $2)
        ''', platform, platform_id)

    async def delete(self, platform: str, platform_id: str) -> None:
        await self.database.execute('''
            DELETE from users
            WHERE platform = ($1) and platform_id = ($2)
        ''', platform, platform_id)
