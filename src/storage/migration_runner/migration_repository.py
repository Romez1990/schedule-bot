from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Type,
)

from storage.migration_runner import Migration


class MigrationRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> Sequence[Type[Migration]]: ...
