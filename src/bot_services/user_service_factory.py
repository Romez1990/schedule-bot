from src.database import UserRepositoryInterface
from .user_service_factory_interface import UserServiceFactoryInterface
from .user_settings_service_interface import UserSettingsServiceInterface
from .subscription_service_interface import SubscriptionServiceInterface
from .user_service_interface import UserServiceInterface
from .user_service import UserService


class UserServiceFactory(UserServiceFactoryInterface):
    def __init__(self, users: UserRepositoryInterface, user_settings_service: UserSettingsServiceInterface,
                 subscription_service: SubscriptionServiceInterface) -> None:
        self.__users = users
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service

    def create(self, platform: str) -> UserServiceInterface:
        return UserService(self.__users, self.__user_settings_service, self.__subscription_service, platform)
