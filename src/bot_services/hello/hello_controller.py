from messenger_services.messenger_service import (
    MessengerController,
    MessengerAdapter,
    Message,
    Keyboard,
    Button,
    controller,
    message_handler,
)
from .chat_service import ChatService


@controller
class HelloController(MessengerController):
    def __init__(self, adapter: MessengerAdapter, chat_service: ChatService) -> None:
        super().__init__(adapter)
        self.__chat_service = chat_service

    @message_handler('start')
    async def start(self, message: Message) -> None:
        await self.__chat_service.add_chat(self._messenger, message.chat)
        keyboard = self.__get_main_menu_keyboard()
        await self._send_message(message.chat, 'Добро пожаловать в мир расписания', keyboard)

    @message_handler('Назад')
    async def back_to_main_menu(self, message: Message) -> None:
        keyboard = self.__get_main_menu_keyboard()
        await self._send_message(message.chat, '.', keyboard)

    def __get_main_menu_keyboard(self) -> Keyboard:
        keyboard = Keyboard(resize=True)
        keyboard.row(
            Button('Выбрать группу'),
            Button('Выбрать тему'),
        )
        keyboard.row(
            Button('Тек. расписание'),
            Button('След. расписание'),
        )
        return keyboard

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.chat, 'Sorry, I have not been taught to help yet')
