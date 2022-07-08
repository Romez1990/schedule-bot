from messenger_services.messenger_service import (
    MessengerController,
    Message,
    Keyboard,
    InlineKeyboard,
    Button,
    InlineButton,
    Payload,
    controller,
    message_handler,
)
from .payloads import (
    DeleteGroupPayload,
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
        await self._send_message(message.chat, 'Welcome to the world of schedule', keyboard)

    @message_handler('Выбрать группу')
    async def select_group(self, message: Message) -> None:
        groups = [
            'ИС-20-Д',
            'ИС-19-Д',
        ]
        keyboard = InlineKeyboard()
        for group in groups:
            keyboard.row(
                InlineButton(group, payload=Payload.none),
                InlineButton('Удалить', payload=DeleteGroupPayload(group)),
            )
        await self._send_message(message.chat, 'Добавленные группы:', keyboard)

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.chat, 'Sorry, I have not been taught to help yet')
