from data.fp.task import taskify
from data.vector import List
from storage.entities import (
    User,
    GroupSubscription,
)
from storage.database import (
    Record,
)
from .repository_base import RepositoryBase
from .group_subscription_repository import GroupSubscriptionRepository


class GroupSubscriptionRepositoryImpl(GroupSubscriptionRepository, RepositoryBase):
    @taskify
    async def save(self, group_subscription: GroupSubscription) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO group_subscriptions(user_id, group_name)
                VALUES ($1, $2)
            ''', group_subscription.user.id, group_subscription.group_name)

    async def delete(self, group_subscription: GroupSubscription) -> None:
        async with self._get_connection() as connection:
            await connection.execute('''
                DELETE FROM group_subscriptions WHERE id = $1
            ''', group_subscription.id)

    async def find_all(self, user: User) -> List[GroupSubscription]:
        async with self._get_connection() as connection:
            group_subscription = await connection.fetch('''
                SELECT * FROM group_subscriptions
                WHERE user_id = $1
            ''', user.id)
            return List(group_subscription) \
                .map(self.__create_group_subscription)

    def __create_group_subscription(self, record: Record) -> GroupSubscription:
        return GroupSubscription(**record)
