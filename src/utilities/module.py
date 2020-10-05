from src.ioc_container import Module, ContainerBuilder
from .list_helper import ListHelper


class UtilitiesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(ListHelper).to_self()
