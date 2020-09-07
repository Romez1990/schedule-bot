from os import getenv

import asyncio
import asyncpg

DB_HOST = 'localhost'
DB_NAME = 'schedule_bot_db'
DB_USER = getenv('DB_USER_SCHEDULE_BOT')
DB_PASS = getenv('DB_PASS_SCHEDULE_BOT')


class Database:
    def __init__(self):
        pass

    async def connect_to_database(self) -> asyncpg.connection:
        connect = await asyncpg.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

        try:
            if connect:
                return connect
            else:
                return None
        except asyncpg as ex:
            return f"Случилась ошибка, {ex}"

    async def add_data_to_table_users_subscribe(self, username: str, subscribe: bool) -> None:
        connect = await self.connect_to_database()
        await connect.execute('''
            INSERT INTO users_subscribe(username, subscribe) VALUES($1, $2)  
        ''', username, subscribe)
        await connect.close()

    async def delete_from_table_users_subscribe(self, username: str, subscribe: bool) -> None:
        connect = await self.connect_to_database()
        await connect.execute('''
            DELETE FROM users_subscribe
            WHERE username = ($1) and subscribe = ($2)
        ''', username, subscribe)
        await connect.close()


database = Database()
add = database.add_data_to_table_users_subscribe('Kuat22222222', True)
delete = database.delete_from_table_users_subscribe('Kuat', True)

asyncio.get_event_loop().run_until_complete(add)
