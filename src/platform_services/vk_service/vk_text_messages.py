from .vk_text_messages_interface import VkBotMessagesInterface
from src.platform_services.text_messages.bot_text_messages_interface import BotTextMessagesInterface
from ..text_messages.primitives import TextComponent


class VkTextMessages(VkBotMessagesInterface):
    def __init__(self, bot_text_messages: BotTextMessagesInterface) -> None:
        self.__bot_text_messages = bot_text_messages

    @property
    def start(self) -> TextComponent:
        return self.__bot_text_messages.start

    @property
    def help(self) -> TextComponent:
        return self.__bot_text_messages.help

    def subscribe(self, group_name: str) -> TextComponent:
        return self.__bot_text_messages.subscribe(group_name)

    def unsubscribe(self, group_name: str) -> TextComponent:
        return self.__bot_text_messages.unsubscribe(group_name)

    def theme(self, theme: str) -> TextComponent:
        return self.__bot_text_messages.theme(theme)
