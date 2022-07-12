from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from storage.repositories import (
    GroupSubscriptionRepository,
)
from storage.entities import (
    GroupSubscription,
)
from messenger_services.messenger_service import (
    Chat,
)
from .group_service import GroupService
from bot_services.hello.chat_service import ChatService


@service
class GroupServiceImpl(GroupService):
    def __init__(self, chat_service: ChatService, group_subscriptions: GroupSubscriptionRepository) -> None:
        self.__chat_service = chat_service
        self.__group_subscriptions = group_subscriptions

    async def get_groups(self, chat: Chat) -> Sequence[str]:
        chat_entity = await self.__chat_service.find(chat)
        group_subscriptions = await self.__group_subscriptions.find_all_by_chat(chat_entity)
        return group_subscriptions.map(self.__get_group_name)

    def __get_group_name(self, group_subscription: GroupSubscription) -> str:
        return group_subscription.group_name

    async def add_group(self, chat: Chat, group: str) -> None:
        chat_entity = await self.__chat_service.find(chat)
        group_subscription = GroupSubscription(chat_entity.id, group)
        await self.__group_subscriptions.save(group_subscription)

    async def delete_group(self, chat: Chat, group_name: str) -> None:
        chat_entity = await self.__chat_service.find(chat)
        await self.__group_subscriptions.delete_by_group_name(chat_entity, group_name)
