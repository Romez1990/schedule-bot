from ..database import Database


class UserSubscribe:
    def __init__(self, database: Database):
        self.database = database

    async def add(self, user_id: int, group_name: str) -> None:
        """
        Here I call execute from database.py and add data for tables a `subscriptions`
        :param user_id:
        :param group_name:
        :return:
        """
        await self.database.execute('''
            INSERT INTO "subscriptions "(user_id, "group") VALUES ($1, $2)
        ''', user_id, group_name)

    async def delete(self, user_id: int, group_name: str) -> None:
        """
        Here I cal execute from database.py and delete dates from a tables `subscriptions`
        :param user_id:
        :param group_name:
        :return:
        """
        await self.database.execute('''
            DELETE from "subscriptions "
            WHERE "user_id" = ($1) and "group" = ($1)
        ''', user_id, group_name)
