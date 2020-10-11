from src.ioc_container import Module, Container
from .user_repository_interface import UserRepositoryInterface
from .user_repository import UserRepository
from .user_settings_repository_interface import UserSettingsRepositoryInterface
from .user_settings_repository import UserSettingsRepository
from .subscription_repository_interface import SubscriptionRepositoryInterface
from .subscription_repository import SubscriptionRepository


class RepositoriesModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(UserRepository).to(UserRepositoryInterface)
        container.bind(UserSettingsRepository).to(UserSettingsRepositoryInterface)
        container.bind(SubscriptionRepository).to(SubscriptionRepositoryInterface)
