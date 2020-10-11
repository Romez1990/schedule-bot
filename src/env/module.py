from src.ioc_container import Module, ContainerBuilder
from .environment_interface import EnvironmentInterface
from .environment import Environment
from .environment_driver import EnvironmentDriver
from .dot_env_environment_driver import DotEnvEnvironmentDriver


class EnvModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(Environment).to(EnvironmentInterface)
        builder.bind(DotEnvEnvironmentDriver).to(EnvironmentDriver)
