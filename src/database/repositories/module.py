from src.ioc_container import Module, ContainerBuilder
from .user_repository_interface import UserRepositoryInterface
from .user_repository import UserRepository
from .user_settings_repository_interface import UserSettingsRepositoryInterface
from .user_settings_repository import UserSettingsRepository
from .subscription_repository_interface import SubscriptionRepositoryInterface
from .subscription_repository import SubscriptionRepository


class RepositoriesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(UserRepository).to(UserRepositoryInterface)
        builder.bind(UserSettingsRepository).to(UserSettingsRepositoryInterface)
        builder.bind(SubscriptionRepository).to(SubscriptionRepositoryInterface)
