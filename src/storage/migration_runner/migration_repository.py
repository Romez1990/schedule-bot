from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Type,
)

from storage.migration_runner import Migration


class MigrationRepository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def migrations(self) -> Sequence[Type[Migration]]: ...
