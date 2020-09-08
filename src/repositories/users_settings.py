from ..database import Database


class UserSettings:
    def __init__(self, database: Database):
         self.database = database

    async def add(self, id: int, theme: str):
        await self.database.execute('''
            INSERT INTO user_settings(user_id, theme) VALUES ($1, $2)
        ''', id, theme)

