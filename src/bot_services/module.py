from src.ioc_container import Module, Container
from .user import UserModule
from .user_settings import UserSettingModule
from .subscription import SubscriptionModule


class BotServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(UserModule)
        container.register_module(UserSettingModule)
        container.register_module(SubscriptionModule)
