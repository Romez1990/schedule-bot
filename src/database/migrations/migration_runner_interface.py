from typing import (
    Iterable,
)

from .migration import Migration


class MigrationRunnerInterface:
    async def run(self, migrations: Iterable[Migration]) -> None:
        raise NotImplementedError
