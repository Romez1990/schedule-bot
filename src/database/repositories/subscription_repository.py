from typing import List

from ...entities import User, Subscription
from ..abscrtract_database import AbstractDatabase
from .abstract_subscription_repository import AbstractSubscriptionRepository


class SubscriptionRepository(AbstractSubscriptionRepository):
    def __init__(self, database: AbstractDatabase):
        self.__database = database

    async def save(self, subscription: Subscription) -> Subscription:
        await self.__database.execute('''
            INSERT INTO subscriptions (user_id, "group")
            VALUES ($1, $2)
        ''', subscription.user.id, subscription.group)
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        await self.__database.execute('''
            DELETE from subscriptions
            WHERE user_id = $1 AND "group" = $2
        ''', subscription.user.id, subscription.group)

    async def find_by_user(self, user: User) -> List[Subscription]:
        records = await self.__database.fetch('''
            SELECT "group" FROM subscriptions
            WHERE user_id = $1
        ''', user.id)
        return [Subscription(user, **record) for record in records]
