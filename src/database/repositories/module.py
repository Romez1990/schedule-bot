from ...ioc_container import Module, ContainerBuilder
from .abstract_user_repository import AbstractUserRepository
from .user_repository import UserRepository
from .abstract_user_settings_repository import AbstractUserSettingsRepository
from .user_settings_repository import UserSettingsRepository
from .abstract_subscription_repository import AbstractSubscriptionRepository
from .subscription_repository import SubscriptionRepository


class RepositoriesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractUserRepository).to(UserRepository)
        builder.bind(AbstractUserSettingsRepository).to(UserSettingsRepository)
        builder.bind(AbstractSubscriptionRepository).to(SubscriptionRepository)
