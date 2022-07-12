from messenger_services.messenger_service import (
    MessengerController,
    MessengerAdapter,
    Message,
    Callback,
    Chat,
    KeyboardBase,
    Keyboard,
    InlineKeyboard,
    Button,
    InlineButton,
    controller,
    message_handler,
    callback_handler,
)
from .group_service import GroupService
from .payloads import (
    SelectCoursePayload,
    AddGroupPayload,
    DeleteGroupPayload,
)


@controller
class GroupController(MessengerController):
    def __init__(self, adapter: MessengerAdapter, group_service: GroupService) -> None:
        super().__init__(adapter)
        self.__group_service = group_service

    @message_handler('Выбрать группу')
    async def manage_groups(self, message: Message) -> None:
        keyboard = await self.__get_groups_keyboard(message.chat)
        await self._send_message(message.chat, 'Добавленные группы:', keyboard)
        keyboard = Keyboard(resize=True)
        keyboard.row(
            Button('Добавить группу'),
            Button('Назад'),
        )
        await self._send_message(message.chat, '.', keyboard)

    @message_handler('Добавить группу')
    async def select_course(self, message: Message) -> None:
        keyboard = InlineKeyboard()
        for course_number in range(1, 4 + 1):
            keyboard.row(InlineButton(f'{course_number} курс', payload=SelectCoursePayload(course_number)))
        await self._send_message(message.chat, 'Выберете курс', keyboard)

    @callback_handler(SelectCoursePayload)
    async def select_group(self, callback: Callback[SelectCoursePayload]) -> None:
        groups = {
            1: ['ИС-21-Д', 'ПГ-21-Д', 'АЭС-21-Д'],
            2: ['ИС-20-Д', 'ПГ-20-Д', 'АЭС-20-Д'],
            3: ['COVID-19-Д', 'ПГ-19-Д', 'АЭС-19-Д'],
            4: ['ИС-18-Д', 'ПГ-18-Д', 'АЭС-18-Д'],
        }
        await callback.answer('')
        groups_by_course = groups[callback.payload.course]
        keyboard = InlineKeyboard()
        for group in groups_by_course:
            keyboard.row(InlineButton(group, payload=AddGroupPayload(group)))
        await self._send_message(callback.chat, 'Выберете группу', keyboard)

    @callback_handler(AddGroupPayload)
    async def add_group(self, callback: Callback[AddGroupPayload]) -> None:
        await self.__group_service.add_group(callback.chat, callback.payload.group)
        await callback.answer(f'Группа {callback.payload.group} добавлена')
        keyboard = Keyboard(resize=True)
        keyboard.row(
            Button('Выбрать группу'),
            Button('Выбрать тему'),
        )
        keyboard.row(
            Button('Тек. расписание'),
            Button('След. расписание'),
        )
        await self._send_message(callback.chat, '.', keyboard)

    @callback_handler(DeleteGroupPayload)
    async def delete_group(self, callback: Callback[DeleteGroupPayload]) -> None:
        await self.__group_service.delete_group(callback.chat, callback.payload.group)
        await callback.answer(f'Группа {callback.payload.group} удалена')
        keyboard = await self.__get_groups_keyboard(callback.chat)
        await self._send_message(callback.chat, 'Добавленные группы:', keyboard)
        keyboard = Keyboard(resize=True)
        keyboard.row(
            Button('Добавить группу'),
            Button('Назад'),
        )
        await self._send_message(callback.chat, '.', keyboard)

    async def __get_groups_keyboard(self, chat: Chat) -> KeyboardBase:
        groups = await self.__group_service.get_groups(chat)
        keyboard = InlineKeyboard()
        if len(groups) == 0:
            keyboard.row(InlineButton('Нет добавленных групп'))
        for group in groups:
            keyboard.row(
                InlineButton(group),
                InlineButton('Удалить', payload=DeleteGroupPayload(group)),
            )
        return keyboard
