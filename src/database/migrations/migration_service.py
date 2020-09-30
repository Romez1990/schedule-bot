from .abstract_migration_service import AbstractMigrationService
from .abstract_migration_repository import AbstractMigrationRepository
from .abstract_migration_runner import AbstractMigrationRunner


class MigrationService(AbstractMigrationService):
    def __init__(self, migration_repository: AbstractMigrationRepository,
                 migration_runner: AbstractMigrationRunner) -> None:
        self.__migration_repository = migration_repository
        self.__migration_runner = migration_runner

    async def run(self) -> None:
        migrations = self.__migration_repository.get_all()
        await self.__migration_runner.run(migrations)
