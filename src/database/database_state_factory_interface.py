from asyncpg import Connection

from .database_state import DatabaseState


class DatabaseStateFactoryInterface:
    def create_disconnected_database(self) -> DatabaseState:
        raise NotImplementedError

    def create_connected_database(self, connection: Connection) -> DatabaseState:
        raise NotImplementedError
