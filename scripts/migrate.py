from infrastructure.script_runner import AsyncScript, script
from storage.migration_runner import MigrationRunner


@script
class MigrateScript(AsyncScript):
    def __init__(self, migration_runner: MigrationRunner) -> None:
        self.__migration_runner = migration_runner

    async def run(self) -> None:
        await self.__migration_runner.run()
