from infrastructure.ioc_container import service
from data.fp.task import taskify
from data.vector import List
from storage.entities import (
    Chat,
    GroupSubscription,
)
from storage.database import (
    Record,
)
from .repository_base import RepositoryBase
from .group_subscription_repository import GroupSubscriptionRepository


@service
class GroupSubscriptionRepositoryImpl(GroupSubscriptionRepository, RepositoryBase):
    async def find_all_by_chat(self, chat: Chat) -> List[GroupSubscription]:
        async with self._get_connection() as connection:
            group_subscription = await connection.fetch('''
                SELECT * FROM group_subscriptions
                WHERE chat_id = $1
            ''', chat.id)
            return List(group_subscription) \
                .map(self.__create_group_subscription)

    @taskify
    async def save(self, group_subscription: GroupSubscription) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO group_subscriptions(chat_id, group_name)
                VALUES ($1, $2)
            ''', group_subscription.chat_id, group_subscription.group_name)

    async def delete_by_group_name(self, chat: Chat, group_name: str) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                DELETE FROM group_subscriptions WHERE chat_id = $1 AND group_name = $2
            ''', chat.id, group_name)

    def __create_group_subscription(self, record: Record) -> GroupSubscription:
        return GroupSubscription(**record)
