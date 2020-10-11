from src.ioc_container import Module, Container
from .telegram_service import TelegramServiceModule
from .vk_service import VkServiceModule


class PlatformServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(TelegramServiceModule)
        container.register_module(VkServiceModule)
