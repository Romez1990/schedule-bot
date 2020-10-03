from asyncio import get_event_loop, AbstractEventLoop

from src.app_container_builder import AppContainerBuilder
from src.env import AbstractEnvironment
from src.database import Database
from src.platform_services import TelegramService, VkService


async def main(loop: AbstractEventLoop) -> None:
    """
    This function for init then we transfer it to main.py in root directory
    :return: None
    """
    container_builder = AppContainerBuilder()
    container = container_builder.build()

    env = container.get(AbstractEnvironment)
    database = container.get(Database)
    telegram_service = container.get(TelegramService)
    vk_service = container.get(VkService)

    env.read()
    await database.connect()
    loop.create_task(telegram_service.start())
    loop.create_task(vk_service.start())


loop = get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
