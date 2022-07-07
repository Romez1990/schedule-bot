from asyncio import (
    create_task,
    sleep,
)
from typing import (
    NoReturn,
)

from infrastructure.script_runner import AsyncScript, script
from infrastructure.logger import LoggerFactory
from infrastructure.errors import NoReturnError
from data.fp.task import Task
from storage.database import ConnectionPool
from schedule_services.update_checker import ScheduleUpdateService
from messenger_services.messenger_service import MessengerManager


@script
class StartScript(AsyncScript):
    def __init__(self, logger_factory: LoggerFactory,
                 connection_pool: ConnectionPool,
                 schedule_update_service: ScheduleUpdateService,
                 messenger_manager: MessengerManager) -> None:
        self.logger = logger_factory.create()
        self.connection_pool = connection_pool
        self.schedule_update_service = schedule_update_service
        self.messenger_manager = messenger_manager

    async def run(self) -> NoReturn:
        await self.init()
        self.logger.info('App has been started')
        await self.start()

    async def init(self) -> None:
        task = create_task(Task.parallel(
            self.connection_pool.init(),
            self.schedule_update_service.init(),
        ))
        await sleep(0)
        self.messenger_manager.init(self.container)
        await task

    async def start(self) -> NoReturn:
        await Task.parallel(
            self.schedule_update_service.start_checking_for_updates(),
            self.messenger_manager.start(),
        )
        raise NoReturnError
