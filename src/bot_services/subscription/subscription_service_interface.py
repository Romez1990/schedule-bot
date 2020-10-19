from typing import (
    List,
)
from returns.future import FutureResult

from src.schedule import GroupNameParsingError
from src.entities import User, Subscription


class SubscriptionServiceInterface:
    def create(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingError]:
        raise NotImplementedError

    def delete(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingError]:
        raise NotImplementedError

    async def find(self, user: User) -> List[Subscription]:
        raise NotImplementedError
