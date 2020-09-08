from ..database import Database


class UserSubscribe:
    def __init__(self, database: Database):
        self.database = database

    async def add(self, user_id: int, group_name: str) -> None:
        await self.database.execute('''
            INSERT INTO "subscriptions "(user_id, "group") VALUES ($1, $2)
        ''', user_id, group_name)
