from src.ioc_container import Module, Container
from .user_service_factory_interface import UserServiceFactoryInterface
from .user_service_factory import UserServiceFactory


class UserModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(UserServiceFactory).to(UserServiceFactoryInterface)
