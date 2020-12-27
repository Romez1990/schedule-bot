from .environment_interface import EnvironmentInterface
from .environment_state_factory_interface import EnvironmentStateFactoryInterface


class Environment(EnvironmentInterface):
    def __init__(self, environment_state_factory: EnvironmentStateFactoryInterface) -> None:
        self.__environment_state_factory = environment_state_factory
        self.__environment_state = self.__environment_state_factory.create_unread_environment()

    def read(self) -> None:
        self.__environment_state.read()
        self.__environment_state = self.__environment_state_factory.create_read_environment()

    def get_str(self, key: str) -> str:
        return self.__environment_state.get_str(key)

    def get_bool(self, key: str) -> bool:
        return self.__environment_state.get_bool(key)

    def get_int(self, key: str) -> int:
        return self.__environment_state.get_int(key)

    def get_float(self, key: str) -> float:
        return self.__environment_state.get_float(key)
