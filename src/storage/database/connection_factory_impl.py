from infrastructure.ioc_container import service
from infrastructure.config import Config
from .connection_factory import ConnectionFactory
from .connection import Connection
from .postgres_connection import PostgresConnection


@service
class ConnectionFactoryImpl(ConnectionFactory):
    def __init__(self, config: Config) -> None:
        self.__config = config

    def create(self) -> Connection:
        return PostgresConnection(self.__config)
