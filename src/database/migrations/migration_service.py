from .migration_service_interface import MigrationServiceInterface
from .migration_repository_interface import MigrationRepositoryInterface
from .migration_runner_interface import MigrationRunnerInterface


class MigrationService(MigrationServiceInterface):
    def __init__(self, migration_repository: MigrationRepositoryInterface,
                 migration_runner: MigrationRunnerInterface) -> None:
        self.__migration_repository = migration_repository
        self.__migration_runner = migration_runner

    async def run(self) -> None:
        migrations = self.__migration_repository.get_all()
        await self.__migration_runner.run(migrations)
