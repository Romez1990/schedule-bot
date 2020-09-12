from os import getenv

from typing import Any

import asyncpg

HOST = 'localhost'
NAME = 'schedule_bot_db'
USER = getenv('USER_SCHEDULE_BOT')
PASS = getenv('PASS_SCHEDULE_BOT')


class Database:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password

    connection: asyncpg.connection.Connection

    async def connect(self) -> asyncpg.connection:
        """
        This function is responsible for connect to database
        :return: asyncpg.connection
        """
        self.connection = await asyncpg.connect(host=self.host, database=self.name, user=self.user,
                                                password=self.password)

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
