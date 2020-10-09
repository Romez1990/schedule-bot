from typing import (
    Iterable,
)
from asyncpg import DuplicateObjectError

from ..database import Database
from .migration_runner_interface import MigrationRunnerInterface
from .migration import Migration


class MigrationRunner(MigrationRunnerInterface):
    def __init__(self, database: Database) -> None:
        self.__database = database

    async def run(self, migrations: Iterable[Migration]) -> None:
        for migration in migrations:
            await self.__run_create_table_query(migration.create_table)
        for migration in migrations:
            if hasattr(migration, 'create_relationships'):
                await self.__run_create_relationships_query(migration.create_relationships)

    async def __run_create_table_query(self, query: str) -> None:
        await self.__database.execute(query)

    async def __run_create_relationships_query(self, query: str) -> None:
        try:
            await self.__database.execute(query)
        except DuplicateObjectError:
            pass
