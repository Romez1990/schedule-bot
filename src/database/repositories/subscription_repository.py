from src.entities import User, Subscription
from ..database import Database
from .subscription_repository_interface import SubscriptionRepositoryInterface


class SubscriptionRepository(SubscriptionRepositoryInterface):
    def __init__(self, database: Database) -> None:
        self.__database = database

    async def save(self, subscription: Subscription) -> Subscription:
        await self.__database.execute('''
            INSERT INTO subscriptions (user_id, "group")
            VALUES ($1, $2)
        ''', subscription.user.id, str(subscription.group))
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        await self.__database.execute('''
            DELETE from subscriptions
            WHERE user_id = $1 AND "group" = $2
        ''', subscription.user.id, subscription.group)

    async def find_by_user(self, user: User) -> list[Subscription]:
        records = await self.__database.fetch('''
            SELECT "group" FROM subscriptions
            WHERE user_id = $1
        ''', user.id)
        return [Subscription(user, **record) for record in records]
