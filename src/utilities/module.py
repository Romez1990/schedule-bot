from src.ioc_container import Module, Container
from .paths_interface import PathsInterface
from .paths import Paths
from .list_helper import ListHelper


class UtilitiesModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(Paths).to(PathsInterface)
        container.bind(ListHelper).to_self()
