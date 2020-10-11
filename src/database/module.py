from src.ioc_container import Module, Container
from .repositories import RepositoriesModule
from .migrations import MigrationsModule
from .database import Database
from .postgres_database import PostgresDatabase


class DatabaseModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(RepositoriesModule)
        container.register_module(MigrationsModule)
        container.bind(PostgresDatabase).to(Database)
