from typing import (
    Type,
    Callable,
)

from infrastructure.ioc_container import service
from data.vector import List
from data.fp.task import Task
from storage.database import (
    ConnectionPool,
    DataFetcher,
)
from .migration_runner import MigrationRunner
from .migration_run_factory import MigrationRunFactory
from .migration_repository import MigrationRepository
from .migration_run import MigrationRun
from .migration import Migration


@service
class MigrationRunnerImpl(MigrationRunner):
    def __init__(self, connection_pool: ConnectionPool, migration_run_factory: MigrationRunFactory,
                 migrations: MigrationRepository) -> None:
        self.__connection_pool = connection_pool
        self.__migration_run_factory = migration_run_factory
        self.__migrations = migrations.find_all()

    async def run(self) -> None:
        async with self.__connection_pool.get_connection() as connection:
            create_table_tasks = List(self.__migrations) \
                .map(self.__instantiate_migration) \
                .map(self.__create_migration_run(connection)) \
                .map(self.__run_create_table)
            migration_runs = await Task.series(create_table_tasks)
            create_relationship_tasks = List(migration_runs) \
                .map(self.__run_create_relationship)
            await Task.series(create_relationship_tasks)

    def __instantiate_migration(self, migration_class: Type[Migration]) -> Migration:
        return migration_class()

    def __create_migration_run(self, data_fetcher: DataFetcher) -> Callable[[Migration], MigrationRun]:
        def create_migration_run(migration: Migration) -> MigrationRun:
            return self.__migration_run_factory.create(data_fetcher, migration)

        return create_migration_run

    def __run_create_table(self, migration_run: MigrationRun) -> Task[MigrationRun]:
        return migration_run.create_table() \
            .map(lambda _: migration_run)

    def __run_create_relationship(self, migration_run: MigrationRun) -> Task[None]:
        return migration_run.create_relationship()
