from infrastructure.ioc_container import service
from infrastructure.logger import LoggerFactory
from storage.database import (
    Database,
)
from .migration_run_factory import MigrationRunFactory
from .migration_run import MigrationRun
from .migration_run_impl import MigrationRunImpl
from .migration import Migration


@service
class MigrationRunFactoryImpl(MigrationRunFactory):
    def __init__(self, database: Database, logger_factory: LoggerFactory) -> None:
        self.__database = database
        self.__logger_factory = logger_factory

    def create_migration_run(self, migration: Migration) -> MigrationRun:
        return MigrationRunImpl(self.__database, self.__logger_factory, migration)
