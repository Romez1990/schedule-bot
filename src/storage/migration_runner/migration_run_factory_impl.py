from infrastructure.ioc_container import service
from infrastructure.logger import LoggerFactory
from storage.database import (
    DataFetcher,
)
from .migration_run_factory import MigrationRunFactory
from .migration_run import MigrationRun
from .migration_run_impl import MigrationRunImpl
from .migration import Migration


@service
class MigrationRunFactoryImpl(MigrationRunFactory):
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self.__logger_factory = logger_factory

    def create(self, data_fetcher: DataFetcher, migration: Migration) -> MigrationRun:
        return MigrationRunImpl(data_fetcher, self.__logger_factory, migration)
