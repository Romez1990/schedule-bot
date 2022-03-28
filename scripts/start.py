from typing import (
    NoReturn,
)

from infrastructure.script_runner import AsyncScript, script
from infrastructure.logger import LoggerFactory
from infrastructure.errors import NoReturnError
from storage.database import ConnectionPool
from messenger_services.messenger_service import MessageHandlerRegistrar


@script
class StartScript(AsyncScript):
    def __init__(self, logger_factory: LoggerFactory, connection_pool: ConnectionPool,
                 message_handler_registrar: MessageHandlerRegistrar) -> None:
        self.logger = logger_factory.create()
        self.connection_pool = connection_pool
        self.message_handler_registrar = message_handler_registrar

    async def run(self) -> NoReturn:
        await self.connection_pool.init()
        self.message_handler_registrar.register(self.container)
        self.logger.info('App has been started')
        self.message_handler_registrar.start(),
        raise NoReturnError
