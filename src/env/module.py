from ..ioc_container import Module, ContainerBuilder
from .abstract_environment import AbstractEnvironment
from .environment import Environment
from .environment_driver import EnvironmentDriver
from .base_environment import BaseEnvironment


class EnvModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractEnvironment).to(Environment)
        builder.bind(EnvironmentDriver).to(BaseEnvironment)
