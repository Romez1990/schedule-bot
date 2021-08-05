from abc import ABCMeta, abstractmethod
from typing import (
    Type,
)

from storage.migration_runner import Migration


class MigrationRepository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def migrations(self) -> list[Type[Migration]]: ...
