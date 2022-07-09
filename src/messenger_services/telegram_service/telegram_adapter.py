from typing import (
    MutableMapping,
    Callable,
    Type,
    Awaitable,
)
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import (
    Command,
    Text,
)
from aiogram.types import (
    Message as TelegramMessage,
    CallbackQuery,
    Chat as TelegramChat,
)

from data.fp.maybe import Maybe
from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    MessengerAdapter,
    Chat,
    Message,
    Callback,
    KeyboardBase,
    Payload,
    MessageHandlerParams,
    CallbackHandlerParams,
    PayloadSerializer,
)
from .telegram_keyboard_adapter import TelegramKeyboardAdapter
from .filters import CallbackPayloadFilter


class TelegramAdapter(MessengerAdapter):
    def __init__(self, bot: Bot, dispatcher: Dispatcher, keyboard_adapter: TelegramKeyboardAdapter,
                 payload_serializer: PayloadSerializer, json_serializer: JsonSerializer) -> None:
        self.__bot = bot
        self.__dispatcher = dispatcher
        self.__keyboard_adapter = keyboard_adapter
        self.__payload_serializer = payload_serializer
        self.__json_serializer = json_serializer

    async def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> None:
        messenger_keyboard = Maybe.from_optional(keyboard) \
            .map(self.__keyboard_adapter.map_keyboard) \
            .get_or_none()
        await self.__bot.send_message(chat.id, text, reply_markup=messenger_keyboard)

    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None:
        filters = Command(params.command) | Text(params.command)
        messenger_handler = self.__map_message_handler(handler)
        self.__dispatcher.message_handler(filters)(messenger_handler)

    __payload_classes: MutableMapping[str, Type[Payload]] = {}

    def register_callback_handler(self, params: CallbackHandlerParams,
                                  handler: Callable[[Callback, Payload], Awaitable[None]]) -> None:
        self.__payload_classes[params.payload_class.type] = params.payload_class
        filters = CallbackPayloadFilter(self.__json_serializer, params.payload_class)
        messenger_handler = self.__map_callback_handler(handler)
        self.__dispatcher.callback_query_handler(filters)(messenger_handler)

    def __map_message_handler(self, handler: Callable[[Message], Awaitable[None]]
                              ) -> Callable[[TelegramMessage], Awaitable[None]]:
        async def messenger_handler(messenger_message: TelegramMessage) -> None:
            message = self.__map_message(messenger_message)
            await handler(message)

        return messenger_handler

    def __map_callback_handler(self, handler: Callable[[Callback, Payload], Awaitable[None]]
                               ) -> Callable[[CallbackQuery], Awaitable[None]]:
        async def messenger_handler(query: CallbackQuery) -> None:
            callback = self.__map_callback(query)
            payload = self.__map_callback_data(query.data)
            await handler(callback, payload)

        return messenger_handler

    def __map_message(self, message: TelegramMessage) -> Message:
        chat = self.__map_chat(message.chat)
        return Message(chat, message.text)

    def __map_callback(self, query: CallbackQuery) -> Callback:
        message = self.__map_message(query.message)
        answer = self.__map_answer(query.answer)
        return Callback(message, answer)

    def __map_chat(self, chat: TelegramChat) -> Chat:
        return Chat(chat.id)

    def __map_answer(self, answer: Callable[[str], Awaitable[None]]) -> Callable[[str], Awaitable[None]]:
        return answer

    def __map_callback_data(self, data: str) -> Payload:
        return self.__payload_serializer.deserialize(data, self.__payload_classes)
