from src.ioc_container import Module, Container
from .list_helper import ListHelper


class UtilitiesModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(ListHelper).to_self()
