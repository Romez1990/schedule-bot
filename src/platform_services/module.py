from src.ioc_container import Module, Container
from .telegram_service import TelegramServiceModule
from .vk_service import VkServiceModule
from .button_configuration import ButtonConfiguration
from .messages_text import MessageText


class PlatformServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(TelegramServiceModule)
        container.register_module(VkServiceModule)
        container.bind(ButtonConfiguration).to_self()
        container.bind(MessageText).to_self()
