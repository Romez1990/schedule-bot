from ..database import Database


class UserSettings:
    def __init__(self, database: Database):
        self.database = database

    async def add(self, user_id: int, theme: str):
        """
        Here I call execute from database.py and add data for tables a `user_settings`
        :param user_id:
        :param theme:
        :return:
        """
        await self.database.execute('''
            INSERT INTO user_settings(user_id, theme) VALUES ($1, $2)
        ''', user_id, theme)

    async def delete(self, user_id: int, theme: str) -> None:
        """
        Here I cal execute from database.py and delete dates from a tables `user_settings`
        :param theme:
        :param user_id:
        :return:
        """
        await self.database.execute('''
            DELETE from "user_settings"
            WHERE "user_id" = ($1) and "theme" = ($1)
        ''', user_id, theme)
