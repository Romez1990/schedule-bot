from asyncio import run

from src.ioc_container import Container
from src.app_module import AppModule
from src.database import Database, MigrationServiceInterface
from src.env import EnvironmentInterface


async def main() -> None:
    container = Container()
    container.register_module(AppModule)

    env = container.get(EnvironmentInterface)
    database = container.get(Database)
    migration_service = container.get(MigrationServiceInterface)

    env.read()
    await database.connect()
    await migration_service.run()
    await database.disconnect()


run(main())
