from .environment_state_factory_interface import EnvironmentStateFactoryInterface
from .environment_driver import EnvironmentDriver
from .environment_state import EnvironmentState
from .unread_environment import UnreadEnvironment
from .read_environment import ReadEnvironment


class EnvironmentStateFactory(EnvironmentStateFactoryInterface):
    def __init__(self, environment_driver: EnvironmentDriver) -> None:
        self.__environment_driver = environment_driver

    def create_unread_environment(self) -> EnvironmentState:
        return UnreadEnvironment(self.__environment_driver)

    def create_read_environment(self) -> EnvironmentState:
        return ReadEnvironment(self.__environment_driver)
