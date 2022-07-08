from messenger_services.messenger_service import (
    MessengerController,
    Message,
    Keyboard,
    InlineKeyboard,
    Button,
    InlineButton,
    controller,
    message_handler,
)


@controller
class HelloController(MessengerController):
    @message_handler('start')
    async def start(self, message: Message) -> None:
        keyboard = Keyboard(resize=True)
        keyboard.row(
            Button('Выбрать группу'),
            Button('Выбрать тему'),
        )
        keyboard.row(
            Button('Тек. расписание'),
            Button('След. расписание'),
        )
        await self._send_message(message.user, 'Welcome to the world of schedule', keyboard)

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.user, 'Sorry, I have not been taught to help yet')
