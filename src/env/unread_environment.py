from .errors import (
    EnvironmentUnreadError,
)
from .environment_state import EnvironmentState
from .environment_driver import EnvironmentDriver


class UnreadEnvironment(EnvironmentState):
    def __init__(self, environment_driver: EnvironmentDriver) -> None:
        self.__environment_driver = environment_driver

    def read(self) -> None:
        self.__environment_driver.read()

    def get_str(self, key: str) -> str:
        raise EnvironmentUnreadError()

    def get_bool(self, key: str) -> bool:
        raise EnvironmentUnreadError()

    def get_int(self, key: str) -> int:
        raise EnvironmentUnreadError()

    def get_float(self, key: str) -> float:
        raise EnvironmentUnreadError()
