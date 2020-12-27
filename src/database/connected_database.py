from returns.maybe import Maybe
from asyncpg import Connection, Record

from .database_state import DatabaseState
from .errors import (
    DatabaseAlreadyConnectedError,
)


class ConnectedDatabase(DatabaseState):
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    async def connect(self) -> Connection:
        raise DatabaseAlreadyConnectedError()

    async def disconnect(self) -> None:
        await self.__connection.close()

    async def execute(self, query: str, *args: any) -> None:
        await self.__connection.execute(query, *args)

    async def fetch(self, query: str, *args: any) -> list[dict[str, any]]:
        records = await self.__connection.fetch(query, *args)
        return [self.__record_to_dict(record) for record in records]

    async def fetch_row(self, query: str, *args: any) -> Maybe[dict[str, any]]:
        record = await self.__connection.fetchrow(query, *args)
        maybe_record: Maybe[Record] = Maybe.from_value(record)
        return maybe_record.map(self.__record_to_dict)

    async def fetch_value(self, query: str, *args: any) -> any:
        return await self.__connection.fetchval(query, *args)

    def __record_to_dict(self, record: Record) -> dict[str, any]:
        return {**record}
