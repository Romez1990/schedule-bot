from asyncio import get_event_loop, AbstractEventLoop

from src.ioc_container import Container
from src.app_module import AppModule
from src.env import EnvironmentInterface
from src.database import Database
from src.platform_services import TelegramService, VkService


async def main(loop: AbstractEventLoop) -> None:
    container = Container()
    container.register_module(AppModule)

    env = container.get(EnvironmentInterface)
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
