from returns.maybe import Nothing

from src.database import UserRepositoryInterface
from src.entities import User
from ..user_settings_service_interface import UserSettingsServiceInterface
from ..subscription_service_interface import SubscriptionServiceInterface
from .user_service_interface import UserServiceInterface


class UserService(UserServiceInterface):
    def __init__(self, users: UserRepositoryInterface, user_settings_service: UserSettingsServiceInterface,
                 subscription_service: SubscriptionServiceInterface, platform: str) -> None:
        self.__users = users
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service
        self.__platform = platform

    async def create_if_not_exists(self, platform_id: str) -> bool:
        maybe_user = await self.__users.find(self.__platform, platform_id)
        if maybe_user != Nothing:
            return False
        await self.__create_user(platform_id)
        return True

    async def __create_user(self, platform_id: str) -> None:
        user = User(self.__platform, platform_id)
        user = await self.__users.save(user)
        await self.__user_settings_service.create_default_settings(user)

    async def find_user(self, platform_id: str, *,
                        find_settings: bool = False, find_subscriptions: bool = False) -> User:
        user = (await self.__users.find(self.__platform, platform_id)).unwrap()
        user_settings = (await self.__user_settings_service.find(user)) if find_settings else None
        subscriptions = (await self.__subscription_service.find(user)) if find_subscriptions else None
        return User(user.platform, user.platform_id, user.id, user_settings, subscriptions)
