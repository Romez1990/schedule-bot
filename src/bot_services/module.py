from src.ioc_container import Module, Container
from .user import UserModule
from .user_settings_service_interface import UserSettingsServiceInterface
from .user_settings_service import UserSettingsService
from .subscription_service_interface import SubscriptionServiceInterface
from .subscription_service import SubscriptionService


class BotServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(UserModule)
        container.bind(UserSettingsService).to(UserSettingsServiceInterface)
        container.bind(SubscriptionService).to(SubscriptionServiceInterface)
