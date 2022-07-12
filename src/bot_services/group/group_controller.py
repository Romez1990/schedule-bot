from messenger_services.messenger_service import (
    MessengerController,
    Message,
    Callback,
    KeyboardBase,
    InlineKeyboard,
    InlineButton,
    controller,
    message_handler,
    callback_handler,
)
from .payloads import (
    DeleteGroupPayload,
)


@controller
class GroupController(MessengerController):
    @message_handler('Выбрать группу')
    async def select_group(self, message: Message) -> None:
        keyboard = self.__get_groups_keyboard()
        await self._send_message(message.chat, 'Добавленные группы:', keyboard)

    @callback_handler(DeleteGroupPayload)
    async def delete_group(self, callback: Callback[DeleteGroupPayload]) -> None:
        await callback.answer(f'Группа {callback.payload.group} удалена')
        keyboard = self.__get_groups_keyboard()
        await self._send_message(callback.chat, 'Добавленные группы:', keyboard)

    def __get_groups_keyboard(self) -> KeyboardBase:
        groups = [
            'ИС-20-Д',
            'ИС-19-Д',
        ]
        keyboard = InlineKeyboard()
        for group in groups:
            keyboard.row(
                InlineButton(group),
                InlineButton('Удалить', payload=DeleteGroupPayload(group)),
            )
        return keyboard
