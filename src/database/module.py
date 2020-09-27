from ..ioc_container import Module, ContainerBuilder
from .abscrtract_database import AbstractDatabase
from .database import Database


class DatabaseModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractDatabase).to(Database)
