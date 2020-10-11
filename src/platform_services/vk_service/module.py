from src.ioc_container import Module, Container
from .vk_service import VkService
from .vk_bot import VkBot
from .vk_controller import VkController


class VkServiceModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(VkService).to_self()
        container.bind(VkBot).to_self()
        container.bind(VkController).to_self()
