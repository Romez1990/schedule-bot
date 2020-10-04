from src.ioc_container import Module, ContainerBuilder
from .vk_service import VkService
from .vk_bot import VkBot
from .vk_controller import VkController


class VkServiceModule(Module):
    def _load(self, builder: ContainerBuilder):
        builder.bind(VkService).to_self()
        builder.bind(VkBot).to_self()
        builder.bind(VkController).to_self()
