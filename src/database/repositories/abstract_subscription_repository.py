from typing import (
    List,
)

from src.entities import User, Subscription


class AbstractSubscriptionRepository:
    async def save(self, subscription: Subscription) -> Subscription:
        raise NotImplementedError

    async def delete(self, subscription: Subscription) -> None:
        raise NotImplementedError

    async def find_by_user(self, user: User) -> List[Subscription]:
        raise NotImplementedError
