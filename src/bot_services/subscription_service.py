from typing import List
from returns.future import FutureResult

from ..schedule import Group, AbstractGroupParser, GroupNameParsingException
from ..repositories import AbstractSubscriptionRepository
from ..entities import User, Subscription
from .abstract_subscription_service import AbstractSubscriptionService


class SubscriptionService(AbstractSubscriptionService):
    def __init__(self, subscriptions: AbstractSubscriptionRepository, group_parser: AbstractGroupParser):
        self.__subscriptions = subscriptions
        self.__group_parser = group_parser

    def create(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingException]:
        group_parse_result = self.__group_parser.parse(group_name)
        return FutureResult.from_result(group_parse_result) \
            .bind_awaitable(lambda group: self.__create_and_save_subscription(user, group))

    async def __create_and_save_subscription(self, user: User, group: Group) -> None:
        subscription = Subscription(user, group)
        await self.__subscriptions.save(subscription)

    async def delete(self, subscription: Subscription) -> None:
        await self.__subscriptions.delete(subscription)

    async def find(self, user: User) -> List[Subscription]:
        return await self.__subscriptions.find_by_user(user)
