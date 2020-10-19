from src.ioc_container import Module, Container
from .user import UserModule
from .user_settings import UserSettingModule
from .subscription_service_interface import SubscriptionServiceInterface
from .subscription_service import SubscriptionService


class BotServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(UserModule)
        container.register_module(UserSettingModule)
        container.bind(SubscriptionService).to(SubscriptionServiceInterface)
