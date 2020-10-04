from src.ioc_container import Module, ContainerBuilder
from .repositories import RepositoriesModule
from .migrations import MigrationsModule
from .database import Database
from .postgres_database import PostgresDatabase


class DatabaseModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(RepositoriesModule)
        builder.register_module(MigrationsModule)
        builder.bind(Database).to(PostgresDatabase)
