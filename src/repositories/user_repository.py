from ..database import Database


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    async def add(self, platform: str, platform_id: str) -> None:
        """
        Here I call execute from database.py and add data for tables a `users`
        :param platform:
        :param platform_id:
        :return:
        """
        await self.database.execute('''
            INSERT INTO users(platform, platform_id) VALUES ($1, $2)
        ''', platform, platform_id)

    async def delete(self, platform: str, platform_id: str) -> None:
        """
        Here I call execute from database.py and delete data for tables a `users`
        :param platform:
        :param platform_id:
        :return:
        """
        await self.database.execute('''
            DELETE from users
            WHERE platform = ($1) and platform_id = ($2)
        ''', platform, platform_id)
