from os import getenv

from typing import Any

import asyncpg

DB_HOST = 'localhost'
DB_NAME = 'schedule_bot_db'
DB_USER = getenv('DB_USER_SCHEDULE_BOT')
DB_PASS = getenv('DB_PASS_SCHEDULE_BOT')


class Database:
    def __init__(self):
        pass

    connection: asyncpg.connection.Connection

    async def connect(self) -> asyncpg.connection:
        """
        This function is responsible for connect to database
        :return: asyncpg.connection
        """
        self.connection = await asyncpg.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

        try:
            if self.connection:
                return self.connection
            else:
                return None
        except asyncpg as ex:
            return f"Случилась ошибка, {ex}"

    async def execute(self, sql: str, *args: Any) -> str:
        """
        This function is responsible for execute SQL query to database
        :param sql: string
        :param args: Any
        :return: string in SQL format
        """
        return await self.connection.execute(sql, *args)
