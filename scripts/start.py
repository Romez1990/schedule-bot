from infrastructure.script import AsyncScript, script
from infrastructure.logger import LoggerFactory
from messenger_services.messenger_service import MessageHandlerRegistrar


@script
class StartScript(AsyncScript):
    def __init__(self, logger_factory: LoggerFactory, message_handler_registrar: MessageHandlerRegistrar) -> None:
        self.logger = logger_factory.create('scripts.start')
        self.message_handler_registrar = message_handler_registrar

    async def run(self) -> None:
        self.message_handler_registrar.register(self.container)
        self.logger.info('App has been started')
        await self.message_handler_registrar.start()
