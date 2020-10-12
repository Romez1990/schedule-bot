from src.ioc_container import Module, Container
from .user_service_factory_interface import UserServiceFactoryInterface
from .user_service_factory import UserServiceFactory
from .user_service_interface import UserServiceInterface
from .user_service import UserService
from .user_settings_service_interface import UserSettingsServiceInterface
from .user_settings_service import UserSettingsService
from .subscription_service_interface import SubscriptionServiceInterface
from .subscription_service import SubscriptionService


class BotServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(UserServiceFactory).to(UserServiceFactoryInterface)
        container.bind(UserService).to(UserServiceInterface)
        container.bind(UserSettingsService).to(UserSettingsServiceInterface)
        container.bind(SubscriptionService).to(SubscriptionServiceInterface)
