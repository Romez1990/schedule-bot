from src.ioc_container import Module, Container
from .subscription_service_interface import SubscriptionServiceInterface
from .subscription_service import SubscriptionService


class SubscriptionModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(SubscriptionService).to(SubscriptionServiceInterface)
