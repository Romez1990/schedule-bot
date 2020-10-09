from src.ioc_container import Module, ContainerBuilder
from .user_service_interface import UserServiceInterface
from .user_service import UserService
from .user_settings_service_interface import UserSettingsServiceInterface
from .user_settings_service import UserSettingsService
from .subscription_service_interface import SubscriptionServiceInterface
from .subscription_service import SubscriptionService


class BotServicesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(UserServiceInterface).to(UserService)
        builder.bind(UserSettingsServiceInterface).to(UserSettingsService)
        builder.bind(SubscriptionServiceInterface).to(SubscriptionService)
