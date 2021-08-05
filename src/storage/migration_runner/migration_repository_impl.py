from typing import (
    Type,
)

from infrastructure.ioc_container import service
from .migration_repository import MigrationRepository
from .migration import Migration
from .migration_decorator import migrations


@service
class MigrationRepositoryImpl(MigrationRepository):
    @property
    def migrations(self) -> list[Type[Migration]]:
        return migrations
