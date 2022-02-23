from typing import (
    Coroutine,
    Type,
    TypeVar,
)
from asyncpg import (
    Connection as AsyncpgConnection,
    Record as AsyncpgRecord,
    connect,
    PostgresSyntaxError,
    DuplicateTableError,
    DuplicateObjectError,
)

from infrastructure.config import Config
from data.fp.type import cast
from data.fp.maybe import Maybe
from data.fp.task_either import TaskEither
from .errors import (
    DatabaseError,
    QuerySyntaxError,
    TableAlreadyExistsError,
    ObjectAlreadyExistsError,
)
from .connection import Connection
from .data_fetcher import (
    Records,
    Record,
)

T = TypeVar('T')


class PostgresConnection(Connection):
    def __init__(self, config: Config) -> None:
        self.__config = config

    __connection: AsyncpgConnection

    async def open(self) -> None:
        host = self.__config.db_host
        name = self.__config.db_name
        user = self.__config.db_user
        password = self.__config.db_password
        self.__connection = await connect(host=host, database=name, user=user, password=password)

    async def close(self) -> None:
        await self.__connection.close()

    def execute(self, query: str, *args: object) -> TaskEither[DatabaseError, None]:
        async def perform() -> None:
            await self.__connection.execute(query, *args)

        return self.__except_error(perform())

    def fetch(self, query: str, *args: object) -> TaskEither[DatabaseError, Records]:
        async def perform() -> Records:
            records = await self.__connection.fetch(query, *args)
            return [self.__record_to_dict(record) for record in records]

        return self.__except_error(perform())

    def fetch_row(self, query: str, *args: object) -> TaskEither[DatabaseError, Maybe[Record]]:
        async def perform() -> Maybe[Record]:
            record = await self.__connection.fetchrow(query, *args)
            return Maybe.from_optional(record) \
                .map(self.__record_to_dict)

        return self.__except_error(perform())

    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> TaskEither[DatabaseError, T]:
        coroutine = self.__connection.fetchval(query, *args)
        return self.__except_error(coroutine) \
            .map(cast(value_type))

    def __record_to_dict(self, record: AsyncpgRecord) -> Record:
        # return record
        return dict(record)

    def __except_error(self, coroutine: Coroutine[object, object, T]) -> TaskEither[DatabaseError, T]:
        return TaskEither.try_except(coroutine) \
            .map_left(self.__filter_error)

    def __filter_error(self, error: Exception) -> DatabaseError:
        match error:
            case PostgresSyntaxError():
                return QuerySyntaxError(str(error))
            case DuplicateTableError():
                return TableAlreadyExistsError(str(error))
            case DuplicateObjectError():
                return ObjectAlreadyExistsError(str(error))
            case _:
                raise error
