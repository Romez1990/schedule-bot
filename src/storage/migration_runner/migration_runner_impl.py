from infrastructure.ioc_container import service
from data.vector import List
from data.fp.task import Task
from .migration_runner import MigrationRunner
from .migration_run_factory import MigrationRunFactory
from .migration_repository import MigrationRepository
from .migration_run import MigrationRun
from .migration import Migration


@service
class MigrationRunnerImpl(MigrationRunner):
    def __init__(self, migration_run_factory: MigrationRunFactory, migrations: MigrationRepository) -> None:
        self.__migration_run_factory = migration_run_factory
        self.__migrations = migrations.migrations

    async def run(self) -> None:
        tasks = self.__create_migrations() \
            .map(self.__migration_run_factory.create_migration_run) \
            .map(self.__run_migration)
        await Task.parallel(tasks)

    def __create_migrations(self) -> List[Migration]:
        return List(migration() for migration in self.__migrations)

    def __run_migration(self, migration_run: MigrationRun) -> Task[None]:
        return migration_run.create_table() \
            .bind(lambda _: migration_run.create_relationship())
