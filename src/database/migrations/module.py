from src.ioc_container import Module, ContainerBuilder
from .migration_service_interface import MigrationServiceInterface
from .migration_service import MigrationService
from .migration_repository_interface import MigrationRepositoryInterface
from .migration_repository import MigrationRepository
from .migration_runner_interface import MigrationRunnerInterface
from .migration_runner import MigrationRunner


class MigrationsModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(MigrationService).to(MigrationServiceInterface)
        builder.bind(MigrationRepository).to(MigrationRepositoryInterface)
        builder.bind(MigrationRunner).to(MigrationRunnerInterface)
