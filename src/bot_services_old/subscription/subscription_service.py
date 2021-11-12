from returns.future import FutureResult

from src.database import SubscriptionRepositoryInterface
from src.entities import User, Subscription
from src.schedule import (
    Group,
    GroupParserInterface,
    GroupNameParsingError,
)
from .subscription_service_interface import SubscriptionServiceInterface


class SubscriptionService(SubscriptionServiceInterface):
    def __init__(self, subscriptions: SubscriptionRepositoryInterface, group_parser: GroupParserInterface) -> None:
        self.__subscriptions = subscriptions
        self.__group_parser = group_parser

    def create(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingError]:
        group_result = self.__group_parser.parse(group_name)
        return FutureResult.from_result(group_result) \
            .bind_awaitable(lambda group: self.__save_subscription(user, group))

    def delete(self, user: User, group_name: str) -> FutureResult[None, GroupNameParsingError]:
        group_result = self.__group_parser.parse(group_name)
        return FutureResult.from_result(group_result) \
            .bind_awaitable(lambda group: self.__delete_subscription(user, group))

    async def __save_subscription(self, user: User, group: Group) -> None:
        subscription = Subscription(user, group)
        await self.__subscriptions.save(subscription)

    async def __delete_subscription(self, user: User, group: Group) -> None:
        subscription = Subscription(user, group)
        await self.__subscriptions.delete(subscription)

    async def find(self, user: User) -> list[Subscription]:
        return await self.__subscriptions.find_by_user(user)
