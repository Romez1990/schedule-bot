from typing import (
    List,
)

from .migration import Migration


class AbstractMigrationRepository:
    def get_all(self) -> List[Migration]:
        raise NotImplementedError
