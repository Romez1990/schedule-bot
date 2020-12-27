from returns.maybe import Maybe
from asyncpg import connect, Connection

from src.env import EnvironmentInterface
from .database_state import DatabaseState
from .errors import (
    DatabaseDisconnectedError,
)


class DisconnectedDatabase(DatabaseState):
    def __init__(self, env: EnvironmentInterface) -> None:
        self.__env = env

    async def connect(self) -> Connection:
        host = self.__env.get_str('DB_HOST')
        name = self.__env.get_str('DB_NAME')
        user = self.__env.get_str('DB_USER')
        password = self.__env.get_str('DB_PASSWORD')
        return await connect(host=host, database=name, user=user, password=password)

    async def disconnect(self) -> None:
        raise DatabaseDisconnectedError()

    async def execute(self, query: str, *args: any) -> None:
        raise DatabaseDisconnectedError()

    async def fetch(self, query: str, *args: any) -> list[dict[str, any]]:
        raise DatabaseDisconnectedError()

    async def fetch_row(self, query: str, *args: any) -> Maybe[dict[str, any]]:
        raise DatabaseDisconnectedError()

    async def fetch_value(self, query: str, *args: any) -> any:
        raise DatabaseDisconnectedError()
