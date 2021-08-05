from infrastructure.ioc_container import service
from storage.database import (
    Database,
)
from .migration_run_factory import MigrationRunFactory
from .migration_logger import MigrationLogger
from .migration_run import MigrationRun
from .migration_run_impl import MigrationRunImpl
from .migration import Migration


@service
class MigrationRunFactoryImpl(MigrationRunFactory):
    def __init__(self, database: Database, migration_logger: MigrationLogger) -> None:
        self.__database = database
        self.__migration_logger = migration_logger

    def create_migration_run(self, migration: Migration) -> MigrationRun:
        return MigrationRunImpl(self.__database, self.__migration_logger, migration)
