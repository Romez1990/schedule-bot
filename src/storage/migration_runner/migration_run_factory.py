from abc import ABCMeta, abstractmethod

from .migration_run import MigrationRun
from .migration import Migration


class MigrationRunFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_migration_run(self, migration: Migration) -> MigrationRun: ...
