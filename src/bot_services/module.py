from src.ioc_container import Module, ContainerBuilder
from .abstract_user_service import AbstractUserService
from .user_service import UserService
from .abstract_user_settings_service import AbstractUserSettingsService
from .user_settings_service import UserSettingsService
from .abstract_subscription_service import AbstractSubscriptionService
from .subscription_service import SubscriptionService


class BotServicesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractUserService).to(UserService)
        builder.bind(AbstractUserSettingsService).to(UserSettingsService)
        builder.bind(AbstractSubscriptionService).to(SubscriptionService)
