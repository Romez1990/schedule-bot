from .environment_driver import EnvironmentDriver
from .environment_interface import EnvironmentInterface


class Environment(EnvironmentInterface):
    def __init__(self, environment_driver: EnvironmentDriver) -> None:
        self.__environment_driver = environment_driver
        self.__read = False

    def read(self) -> None:
        self.__environment_driver.read()
        self.__read = True

    def get_str(self, key: str) -> str:
        if not self.__read:
            raise EnvironmentError('environment was not read')

        value = self.__environment_driver.get_str(key)
        if value is None:
            raise EnvironmentError(f'no {key} environment variable')
        return value

    def get_bool(self, key: str) -> bool:
        value = self.get_str(key)
        if value == 'true':
            return True
        if value == 'false':
            return False
        raise EnvironmentError(f'key {key} can only be true or false')

    def get_int(self, key: str) -> int:
        value = self.get_str(key)
        return int(value)

    def get_float(self, key: str) -> float:
        value = self.get_str(key)
        return float(value)
