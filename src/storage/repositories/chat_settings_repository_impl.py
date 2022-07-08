from data.fp.task import taskify
from data.vector import List
from storage.entities import (
    Chat,
    ChatSettings,
)
from storage.database import (
    Record,
)
from .repository_base import RepositoryBase
from .chat_settings_repository import ChatSettingsRepository


class ChatSettingsRepositoryImpl(ChatSettingsRepository, RepositoryBase):
    @taskify
    async def save(self, chat_settings: ChatSettings) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO chat_settings(chat_id, name, value)
                VALUES ($1, $2, $3)
            ''', chat_settings.chat.id, chat_settings.name, chat_settings.value)

    async def delete(self, chat_settings: ChatSettings) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                DELETE FROM chat_settings WHERE id = $1
            ''', chat_settings.id)

    async def find_all(self, chat: Chat) -> List[ChatSettings]:
        async with self._get_connection() as connection:
            chat_settings = await connection.fetch('''
                SELECT * FROM chat_settings
                WHERE chat_id = $1
            ''', chat.id)
            return List(chat_settings) \
                .map(self.__create_chat_settings)

    def __create_chat_settings(self, record: Record) -> ChatSettings:
        return ChatSettings(**record)
