from returns.maybe import Nothing

from ..repositories import AbstractUserRepository
from ..entities import User
from .abstract_user_service import AbstractUserService
from .abstract_user_settings_service import AbstractUserSettingsService
from .abstract_subscription_service import AbstractSubscriptionService


class UserService(AbstractUserService):
    def __init__(self, users: AbstractUserRepository, user_settings_service: AbstractUserSettingsService,
                 subscription_service: AbstractSubscriptionService) -> None:
        self.__users = users
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service

    async def create_if_not_exists(self, platform: str, platform_id: str) -> bool:
        maybe_user = await self.__users.find(platform, platform_id)
        if maybe_user != Nothing:
            return False
        await self.__create_user(platform, platform_id)
        return True

    async def __create_user(self, platform: str, platform_id: str) -> None:
        user = User(platform, platform_id)
        user = await self.__users.save(user)
        await self.__user_settings_service.create_default_settings(user)

    async def find_user(self, platform: str, platform_id: str, *,
                        find_settings=False, find_subscriptions=False) -> User:
        user = (await self.__users.find(platform, platform_id)).unwrap()
        user_settings = (await self.__user_settings_service.find(user)) if find_settings else None
        subscriptions = (await self.__subscription_service.find(user)) if find_subscriptions else None
        return User(user.platform, user.platform_id, user.id, user_settings, subscriptions)
