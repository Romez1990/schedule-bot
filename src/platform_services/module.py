from ..ioc_container import Module, ContainerBuilder
from .telegram_service import TelegramServiceModule
from .vk_service import VkServiceModule


class PlatformServicesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(TelegramServiceModule)
        builder.register_module(VkServiceModule)
