from asyncpg import Connection

from src.env import EnvironmentInterface
from .database_state_factory_interface import DatabaseStateFactoryInterface
from .database_state import DatabaseState
from .disconnected_database import DisconnectedDatabase
from .connected_database import ConnectedDatabase


class DatabaseStateFactory(DatabaseStateFactoryInterface):
    def __init__(self, env: EnvironmentInterface) -> None:
        self.__env = env

    def create_disconnected_database(self) -> DatabaseState:
        return DisconnectedDatabase(self.__env)

    def create_connected_database(self, connection: Connection) -> DatabaseState:
        return ConnectedDatabase(connection)
