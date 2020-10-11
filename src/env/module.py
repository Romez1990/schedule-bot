from src.ioc_container import Module, Container
from .environment_interface import EnvironmentInterface
from .environment import Environment
from .environment_driver import EnvironmentDriver
from .dot_env_environment_driver import DotEnvEnvironmentDriver


class EnvModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(Environment).to(EnvironmentInterface)
        container.bind(DotEnvEnvironmentDriver).to(EnvironmentDriver)
