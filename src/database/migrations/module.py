from src.ioc_container import Module, ContainerBuilder
from .abstract_migration_service import AbstractMigrationService
from .migration_service import MigrationService
from .abstract_migration_repository import AbstractMigrationRepository
from .migration_repository import MigrationRepository
from .abstract_migration_runner import AbstractMigrationRunner
from .migration_runner import MigrationRunner


class MigrationsModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractMigrationService).to(MigrationService)
        builder.bind(AbstractMigrationRepository).to(MigrationRepository)
        builder.bind(AbstractMigrationRunner).to(MigrationRunner)
