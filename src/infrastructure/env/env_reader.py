from abc import ABCMeta, abstractmethod
from typing import (
    Optional,
)


class EnvReader(metaclass=ABCMeta):
    @abstractmethod
    def get_str(self, var_name: str) -> Optional[str]: ...
