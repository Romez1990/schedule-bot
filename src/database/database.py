from typing import (
    Any,
    Optional,
    List,
    Dict,
)
from asyncpg import connect, Connection, Record
from returns.maybe import Maybe

from ..env import AbstractEnvironment
from .abscrtract_database import AbstractDatabase
from .database_error import DatabaseError


class Database(AbstractDatabase):
    def __init__(self, env: AbstractEnvironment) -> None:
        self.__env = env
        self.__connection: Optional[Connection] = None

    async def connect(self) -> None:
        host = self.__env.get_str('DB_HOST')
        name = self.__env.get_str('DB_NAME')
        user = self.__env.get_str('DB_USER')
        password = self.__env.get_str('DB_PASSWORD')
        self.__connection = await connect(host=host, database=name, user=user, password=password)

    async def disconnect(self) -> None:
        if self.__connection is None:
            self.__raise_connection_error()
        await self.__connection.close()
        self.__connection = None

    async def execute(self, query: str, *args: Any) -> None:
        if self.__connection is None:
            self.__raise_connection_error()
        await self.__connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> List[Dict[str, Any]]:
        if self.__connection is None:
            self.__raise_connection_error()
        records = await self.__connection.fetch(query, *args)
        return [self.__record_to_dict(record) for record in records]

    async def fetch_row(self, query: str, *args: Any) -> Maybe[Dict[str, Any]]:
        if self.__connection is None:
            self.__raise_connection_error()
        record = await self.__connection.fetchrow(query, *args)
        dict = self.__record_to_dict(record)
        return Maybe.from_value(dict)

    async def fetch_value(self, query: str, *args: Any) -> Any:
        if self.__connection is None:
            self.__raise_connection_error()
        return await self.__connection.fetchval(query, *args)

    def __raise_connection_error(self) -> None:
        raise DatabaseError('database is not connected')

    def __record_to_dict(self, record: Record) -> Dict[str, Any]:
        return {**record}
