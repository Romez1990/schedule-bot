from infrastructure.script import AsyncScript, script
from messenger_services.messenger_service import MessageHandlerRegistrar


@script
class StartScript(AsyncScript):
    def __init__(self, message_handler_registrar: MessageHandlerRegistrar) -> None:
        self.message_handler_registrar = message_handler_registrar

    async def run(self) -> None:
        self.message_handler_registrar.register(self.container)
        print('App has been started')
        await self.message_handler_registrar.start()
