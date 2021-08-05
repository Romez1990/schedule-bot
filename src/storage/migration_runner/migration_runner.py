from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)


class MigrationRunner(metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> Awaitable[None]: ...
