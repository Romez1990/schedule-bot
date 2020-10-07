from asyncio import run

from src.app_container_builder import AppContainerBuilder
from src.database import Database, AbstractMigrationService
from src.env import EnvironmentInterface


async def main() -> None:
    container_builder = AppContainerBuilder()
    container = container_builder.build()

    env = container.get(EnvironmentInterface)
    database = container.get(Database)
    migration_service = container.get(AbstractMigrationService)

    env.read()
    await database.connect()
    await migration_service.run()
    await database.disconnect()


run(main())
