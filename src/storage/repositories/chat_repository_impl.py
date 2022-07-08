from infrastructure.ioc_container import service
from data.fp.maybe import Maybe
from data.fp.task import taskify
from data.fp.task_maybe import task_maybeify
from storage.database import (
    Record,
)
from storage.entities import (
    Chat,
)
from .repository_base import RepositoryBase
from .chat_repository import ChatRepository


@service
class ChatRepositoryImpl(ChatRepository, RepositoryBase):
    @taskify
    async def save(self, chat: Chat) -> Chat:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO chats(messenger, messenger_id)
                VALUES ($1, $2)
            ''', chat.messenger, chat.messenger_id)
            chat_id = await connection.fetch_value('''SELECT currval('chats_id_seq')''', value_type=int)
            return chat.set_id(chat_id)

    @task_maybeify
    async def find(self, messenger: str, messenger_id: str) -> Maybe[Chat]:
        async with self._get_connection() as connection:
            return await connection.fetch_row('''
                SELECT * FROM chats
                WHERE messenger = $1 AND messenger_id = $2
            ''', messenger, messenger_id) \
                .map(self.__create_maybe_chat)

    def __create_maybe_chat(self, maybe_record: Maybe[Record]) -> Maybe[Chat]:
        return maybe_record.map(self.__create_chat)

    def __create_chat(self, record: Record) -> Chat:
        return Chat(**record)
