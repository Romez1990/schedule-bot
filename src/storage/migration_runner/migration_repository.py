from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Type,
)

from storage.migration_runner import Migration


class MigrationRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> Sequence[Type[Migration]]: ...
