from typing import (
    Any,
    List,
    Dict,
)
from asyncpg import connect, Connection, Record
from returns.maybe import Maybe

from src.env import EnvironmentInterface
from .database import Database


class PostgresDatabase(Database):
    def __init__(self, env: EnvironmentInterface) -> None:
        self.__env = env

    __connection: Connection

    async def connect(self) -> None:
        host = self.__env.get_str('DB_HOST')
        name = self.__env.get_str('DB_NAME')
        user = self.__env.get_str('DB_USER')
        password = self.__env.get_str('DB_PASSWORD')
        self.__connection = await connect(host=host, database=name, user=user, password=password)

    async def disconnect(self) -> None:
        await self.__connection.close()
        self.__connection = None

    async def execute(self, query: str, *args: Any) -> None:
        await self.__connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> List[Dict[str, Any]]:
        records = await self.__connection.fetch(query, *args)
        return [self.__record_to_dict(record) for record in records]

    async def fetch_row(self, query: str, *args: Any) -> Maybe[Dict[str, Any]]:
        record = await self.__connection.fetchrow(query, *args)
        maybe_record = Maybe.from_value(record)
        return maybe_record.map(self.__record_to_dict)

    async def fetch_value(self, query: str, *args: Any) -> Any:
        return await self.__connection.fetchval(query, *args)

    def __record_to_dict(self, record: Record) -> Dict[str, Any]:
        return {**record}
