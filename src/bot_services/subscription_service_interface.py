from typing import (
    List,
)
from returns.future import FutureResult

from src.schedule import GroupNameParsingException
from src.entities import User, Subscription


class SubscriptionServiceInterface:
    def create(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingException]:
        raise NotImplementedError

    async def delete(self, subscription: Subscription) -> None:
        raise NotImplementedError

    async def find(self, user: User) -> List[Subscription]:
        raise NotImplementedError