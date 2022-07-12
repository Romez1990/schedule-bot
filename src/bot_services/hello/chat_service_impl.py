from infrastructure.ioc_container import service
from storage.repositories import (
    ChatRepository,
)
from storage.entities import (
    Chat as ChatEntity,
)
from messenger_services.messenger_service import (
    Chat,
)
from .chat_service import ChatService


@service
class ChatServiceImpl(ChatService):
    def __init__(self, chats: ChatRepository) -> None:
        self.__chats = chats

    async def add_chat(self, chat: Chat) -> None:
        chat_maybe = await self.__chats.find(chat.messenger_name, chat.id)
        if chat_maybe.is_some:
            return
        chat_entity = ChatEntity(chat.messenger_name, chat.id)
        await self.__chats.save(chat_entity)

    async def find(self, chat: Chat) -> ChatEntity:
        chat_maybe = await self.__chats.find(chat.messenger_name, chat.id)
        return chat_maybe.get_or_raise()

