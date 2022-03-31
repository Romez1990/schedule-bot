from abc import ABCMeta, abstractmethod

from storage.database import DataFetcher
from .migration_run import MigrationRun
from .migration import Migration


class MigrationRunFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, data_fetcher: DataFetcher, migration: Migration) -> MigrationRun: ...
