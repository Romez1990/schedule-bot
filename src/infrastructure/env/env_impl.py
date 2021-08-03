from infrastructure.ioc_container import service
from .errors import (
    EnvironmentVariableNotFoundError,
    EnvironmentVariableIsEmptyError,
    BooleanEnvironmentVariableError,
    IntegerEnvironmentVariableError,
    PositiveIntegerEnvironmentVariableError,
    FloatEnvironmentVariableError,
    PositiveFloatEnvironmentVariableError,
)
from .env import Env
from .env_reader import EnvReader


@service
class EnvImpl(Env):
    def __init__(self, env_reader: EnvReader) -> None:
        self.__env_reader = env_reader

    def get_str(self, var_name: str) -> str:
        value = self.__env_reader.get_str(var_name)
        if value is None:
            raise EnvironmentVariableNotFoundError(var_name)
        if len(value) == 0:
            raise EnvironmentVariableIsEmptyError(var_name)
        return value

    def get_bool(self, var_name: str) -> bool:
        value = self.get_str(var_name)
        if value == 'true':
            return True
        if value == 'false':
            return False
        raise BooleanEnvironmentVariableError(var_name)

    def get_int(self, var_name: str) -> int:
        value = self.get_str(var_name)
        try:
            int_value = int(value)
        except ValueError:
            raise IntegerEnvironmentVariableError(var_name)
        return int_value

    def get_positive_int(self, var_name: str) -> int:
        value = self.get_int(var_name)
        if value <= 0:
            raise PositiveIntegerEnvironmentVariableError(var_name)
        return value

    def get_float(self, var_name: str) -> float:
        value = self.get_str(var_name)
        try:
            float_value = float(value)
        except ValueError:
            raise FloatEnvironmentVariableError(var_name)
        return float_value

    def get_positive_float(self, var_name: str) -> float:
        value = self.get_float(var_name)
        if value <= 0:
            raise PositiveFloatEnvironmentVariableError(var_name)
        return value
