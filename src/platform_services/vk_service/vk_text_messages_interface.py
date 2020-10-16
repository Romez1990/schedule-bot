from abc import ABCMeta

from src.platform_services.text_messages.platform_service_text_messages import PlatformServiceTextMessages


class VkBotMessagesInterface(PlatformServiceTextMessages, metaclass=ABCMeta):
    pass
