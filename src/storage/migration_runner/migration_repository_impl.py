from typing import (
    Sequence,
    Type,
)

from infrastructure.ioc_container import service
from .migration_repository import MigrationRepository
from .migration import Migration
from .migration_decorator import migrations


@service
class MigrationRepositoryImpl(MigrationRepository):
    def get_all(self) -> Sequence[Type[Migration]]:
        return migrations
