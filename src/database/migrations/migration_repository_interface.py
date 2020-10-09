from typing import (
    List,
)

from .migration import Migration


class MigrationRepositoryInterface:
    def get_all(self) -> List[Migration]:
        raise NotImplementedError
