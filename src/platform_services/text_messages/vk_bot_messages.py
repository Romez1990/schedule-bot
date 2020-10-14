from .vk_bot_messages_interface import VkBotMessagesInterface
from .bot_text_messages import BotTextMessages


class VkBotMessages(VkBotMessagesInterface):
    def __init__(self, bot_text_messages: BotTextMessages) -> None:
        self.bot_text_messages = bot_text_messages

    def __vk_message_text_start(self) -> str:
        return self.bot_text_messages.message_text_start()

    def __vk_message_text_help(self) -> str:
        return self.bot_text_messages.message_text_help()

    def __vk_message_text_subscribe(self, username_group: str) -> str:
        return self.bot_text_messages.message_subscribe(username_group)  # Will need add to argument

    def __vk_message_text_unsubscribe(self, username_group: str) -> str:
        return self.bot_text_messages.message_unsubscribe(username_group)  # Will need add to argument

    def __vk_message_text_theme_selection(self, group: str) -> str:
        return self.bot_text_messages.message_theme(group)  # Will need add to argument
