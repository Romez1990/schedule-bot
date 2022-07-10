from typing import (
    Mapping,
    Callable,
    Awaitable,
)
from vkbottle import (
    GroupEventType,
)
from vkbottle.bot import (
    Bot,
    Message as VkMessage,
    MessageEvent,
)
from vkbottle.dispatch.rules.base import (
    CommandRule,
)

from data.fp.maybe import Maybe
from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    MessengerAdapter,
    Message,
    Callback,
    Chat,
    Payload,
    KeyboardBase,
    MessageHandlerParams,
    CallbackHandlerParams,
    PayloadSerializer,
)
from messenger_services.messenger_service.filters import CallbackPayloadFilter
from .vk_keyboard_adapter import VkKeyboardAdapter
from .vk_filter_adapter import VkFilterAdapter


class VkAdapter(MessengerAdapter):
    def __init__(
            self,
            bot: Bot,
            keyboard_adapter: VkKeyboardAdapter,
            filter_adapter: VkFilterAdapter,
            payload_serializer: PayloadSerializer,
            json_serializer: JsonSerializer,
    ) -> None:
        self.__bot = bot
        self.__api = self.__bot.api
        self.__keyboard_adapter = keyboard_adapter
        self.__filter_adapter = filter_adapter
        self.__payload_serializer = payload_serializer
        self.__json_serializer = json_serializer

    async def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> None:
        messenger_keyboard = Maybe.from_optional(keyboard) \
            .map(self.__keyboard_adapter.map_keyboard) \
            .get_or_none()
        await self.__api.messages.send(chat.id, message=text, keyboard=messenger_keyboard, random_id=0)

    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None:
        rule = CommandRule(params.command, prefixes=['/', ''])
        messenger_handler = self.__map_message_handler(handler)
        self.__bot.on.message(rule)(messenger_handler)

    def register_callback_handler(self, params: CallbackHandlerParams,
                                  handler: Callable[[Callback], Awaitable[None]]) -> None:
        filter = CallbackPayloadFilter(self.__json_serializer, params.payload_class)
        rule = self.__filter_adapter.map_filter(filter, self.__map_callback)
        messenger_handler = self.__map_callback_handler(handler)
        self.__bot.on.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, rule)(messenger_handler)

    def __map_message_handler(self, handler: Callable[[Message], Awaitable[None]]
                              ) -> Callable[[VkMessage], Awaitable[None]]:
        async def messenger_handler(messenger_message: VkMessage) -> None:
            message = self.__map_message(messenger_message)
            await handler(message)

        return messenger_handler

    def __map_callback_handler(self, handler: Callable[[Callback], Awaitable[None]]
                               ) -> Callable[[MessageEvent], Awaitable[None]]:
        async def messenger_handler(event: MessageEvent) -> None:
            callback = self.__map_callback(event)
            await handler(callback)

        return messenger_handler

    def __map_message(self, message: VkMessage) -> Message:
        chat = self.__map_chat_from_message(message)
        return Message(chat, message.text)

    def __map_chat_from_message(self, message: VkMessage) -> Chat:
        return Chat(message.peer_id)

    def __map_callback(self, event: MessageEvent) -> Callback:
        chat = self.__map_chat_from_event(event)
        payload = self.__map_callback_data(event.payload)
        answer = self.__map_answer(event)
        return Callback(chat, payload, answer)

    def __map_chat_from_event(self, event: MessageEvent) -> Chat:
        return Chat(event.peer_id)

    def __map_callback_data(self, data: Mapping[str, object]) -> Payload:
        return self.__payload_serializer.deserialize_from_dict(data)

    def __map_answer(self, event: MessageEvent) -> Callable[[str], Awaitable[None]]:
        async def answer(text: str) -> None:
            event_data = self.__json_serializer.serialize({
                'type': 'show_snackbar',
                'text': text,
            })
            await self.__api.messages.send_message_event_answer(
                event_id=event.event_id,
                peer_id=event.peer_id,
                user_id=event.user_id,
                event_data=event_data,
            )
        return answer
