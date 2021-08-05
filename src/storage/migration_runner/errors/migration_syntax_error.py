from __future__ import annotations
from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from storage.migration_runner import Migration


class MigrationSyntaxError(Exception):
    def __init__(self, migration: Migration, query_name: str) -> None:
        super().__init__(f'In migration {type(migration).__name__} syntax error in "{query_name}" query')
