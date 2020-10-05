from src.ioc_container import Module, ContainerBuilder
from .parser import ParserModule


class ScheduleServicesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(ParserModule)
