from asyncio import create_task
from typing import (
    NoReturn,
)

from infrastructure.script_runner import AsyncScript, script
from infrastructure.logger import LoggerFactory
from infrastructure.errors import NoReturnError
from data.fp.task import Task
from storage.database import ConnectionPool
from schedule_services.update_checker import ScheduleUpdateChecker
from messenger_services.messenger_service import MessageHandlerRegistrar


@script
class StartScript(AsyncScript):
    def __init__(self, logger_factory: LoggerFactory,
                 connection_pool: ConnectionPool,
                 schedule_update_service: ScheduleUpdateChecker,
                 message_handler_registrar: MessageHandlerRegistrar) -> None:
        self.logger = logger_factory.create()
        self.connection_pool = connection_pool
        self.schedule_update_service = schedule_update_service
        self.message_handler_registrar = message_handler_registrar

    async def run(self) -> NoReturn:
        await self.init()
        self.logger.info('App has been started')
        await self.start()

    async def init(self) -> None:
        task = create_task(Task.parallel([
            self.connection_pool.init(),
            self.schedule_update_service.init(),
        ]))
        self.message_handler_registrar.register(self.container)
        await task

    async def start(self) -> NoReturn:
        await Task.parallel([
            self.schedule_update_service.start_checking_for_updates(),
            self.message_handler_registrar.start(),
        ])
        raise NoReturnError
