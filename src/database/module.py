from ..ioc_container import Module, ContainerBuilder
from .repositories import RepositoriesModule
from .migrations import MigrationsModule
from .abscrtract_database import AbstractDatabase
from .database import Database


class DatabaseModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(RepositoriesModule)
        builder.register_module(MigrationsModule)
        builder.bind(AbstractDatabase).to(Database)
