from typing import Iterable
from asyncpg import DuplicateObjectError

from ..database import AbstractDatabase
from .abstract_migration_runner import AbstractMigrationRunner
from .migration import Migration


class MigrationRunner(AbstractMigrationRunner):
    def __init__(self, database: AbstractDatabase, migrations: Iterable[Migration]) -> None:
        self.__migrations = migrations
        self.__database = database

    async def run(self) -> None:
        for migration in self.__migrations:
            await self.__run_create_table_query(migration.create_table)
        for migration in self.__migrations:
            if hasattr(migration, 'create_relationships'):
                await self.__run_create_relationships_query(migration.create_relationships)

    async def __run_create_table_query(self, query: str) -> None:
        await self.__database.execute(query)

    async def __run_create_relationships_query(self, query: str) -> None:
        try:
            await self.__database.execute(query)
        except DuplicateObjectError:
            pass
