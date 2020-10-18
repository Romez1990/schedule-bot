from src.ioc_container import Module, Container
from .telegram_service import TelegramServiceModule
from .vk_service import VkServiceModule
from .text_messages import TextMessagesModule
from .button_configuration import ButtonConfiguration
from .messages_text import MessageText


class PlatformServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(TelegramServiceModule)
        container.register_module(VkServiceModule)
        container.register_module(TextMessagesModule)
        container.bind(ButtonConfiguration).to_self()
        container.bind(MessageText).to_self()
