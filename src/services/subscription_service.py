from ..repositories import UserSubscribe


class SubscriptionService:
    def __init__(self, user_subscription: UserSubscribe):
        self.user_subscription = user_subscription

    async def add(self, user_id, group_name):
        await self.user_subscription.add(user_id, group_name)
