from messenger_services.messenger_service import (
    MessengerController,
    Message,
    controller,
    message_handler,
)


@controller
class HelloController(MessengerController):
    @message_handler('start')
    async def start(self, message: Message) -> None:
        await self._send_message(message.user, 'Welcome to the world of schedule')

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.user, 'Sorry, I have not been taught to help yet')
