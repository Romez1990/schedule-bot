from typing import List

from ..repositories import UserSubscribe


class SubscriptionService:
    def __init__(self, user_subscription: UserSubscribe):
        self.user_subscription = user_subscription

    async def add(self, user_id: int, group_name: str) -> None:
        await self.user_subscription.add(user_id, group_name)

    async def delete(self, user_id: int, group_name: str) -> None:
        await self.user_subscription.delete(user_id, group_name)

    async def change(self, user_id: int, group_name: str) -> None:
        await self.user_subscription.change(user_id, group_name)

    async def check_id(self, user_platform_id: str) -> List:
        await self.user_subscription.check_id(user_platform_id)
