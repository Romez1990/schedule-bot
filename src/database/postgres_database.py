from returns.maybe import Maybe

from .database import Database
from .database_state_factory_interface import DatabaseStateFactoryInterface


class PostgresDatabase(Database):
    def __init__(self, database_state_factory: DatabaseStateFactoryInterface) -> None:
        self.__database_state_factory = database_state_factory
        self.__database_state = self.__database_state_factory.create_disconnected_database()

    async def connect(self) -> None:
        connection = await self.__database_state.connect()
        self.__database_state = self.__database_state_factory.create_connected_database(connection)

    async def disconnect(self) -> None:
        await self.__database_state.disconnect()
        self.__database_state = self.__database_state_factory.create_disconnected_database()

    async def execute(self, query: str, *args: any) -> None:
        await self.__database_state.execute(query, *args)

    async def fetch(self, query: str, *args: any) -> list[dict[str, any]]:
        return await self.__database_state.fetch(query, *args)

    async def fetch_row(self, query: str, *args: any) -> Maybe[dict[str, any]]:
        return await self.__database_state.fetch_row(query, *args)

    async def fetch_value(self, query: str, *args: any) -> any:
        return await self.__database_state.fetch_value(query, *args)
