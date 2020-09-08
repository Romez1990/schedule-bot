from asyncio import run
from os import getenv

import asyncio
from typing import Any, List

import asyncpg

DB_HOST = 'localhost'
DB_NAME = 'schedule_bot_db'
DB_USER = getenv('DB_USER_SCHEDULE_BOT')
DB_PASS = getenv('DB_PASS_SCHEDULE_BOT')


class Database:
    connection: asyncpg.connection.Connection

    async def connect(self) -> asyncpg.connection:
        self.connection = await asyncpg.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

        try:
            if self.connection:
                return self.connection
            else:
                return None
        except asyncpg as ex:
            return f"Случилась ошибка, {ex}"

    async def execute(self, sql: str, *args: Any) -> str:
        return await self.connection.execute(sql, *args)

    # async def add_data_to_table_users_subscribe(self, username: str, subscribe: bool) -> None:
    #     connect = await self.connect()
    #     await connect.execute('''
    #         INSERT INTO users_subscribe(username, subscribe) VALUES($1, $2)
    #     ''', username, subscribe)
    #     await connect.close()
    #
    # async def delete_from_table_users_subscribe(self, username: str, subscribe: bool) -> None:
    #     connect = await self.connect()
    #     await connect.execute('''
    #         DELETE FROM users_subscribe
    #         WHERE username = ($1) and subscribe = ($2)
    #     ''', username, subscribe)
    #     await connect.close()
    #
    # async def add_to_table_users_theme(self, username: str, theme: bool) -> None:
    #     connect = await self.connect()
    #     await connect.execute('''
    #         INSERT INTO users_theme(username, subscribe) VALUES ($1, $2)
    #     ''', username, theme)
    #
    # async def delete_from_table_users_theme(self, username: str, theme):
    #     pass

# database = Database()
# add = database.add_data_to_table_users_subscribe('Kuat222222222321312322', True)
# delete = database.delete_from_table_users_subscribe('Kuat', True)

# asyncio.get_event_loop().run_until_complete(add)

# run(add)
