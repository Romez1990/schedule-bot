from src.ioc_container import Module, Container
from .migration_service_interface import MigrationServiceInterface
from .migration_service import MigrationService
from .migration_repository_interface import MigrationRepositoryInterface
from .migration_repository import MigrationRepository
from .migration_runner_interface import MigrationRunnerInterface
from .migration_runner import MigrationRunner


class MigrationsModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(MigrationService).to(MigrationServiceInterface)
        container.bind(MigrationRepository).to(MigrationRepositoryInterface)
        container.bind(MigrationRunner).to(MigrationRunnerInterface)
