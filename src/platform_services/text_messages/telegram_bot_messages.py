from .telegram_bot_messages_interface import TelegramBotMessagesInterface
from .bot_text_messages import BotTextMessages


class TelegramBotMessages(TelegramBotMessagesInterface):
    def __init__(self, bot_text_messages: BotTextMessages) -> None:
        self.bot_text_messages = bot_text_messages

    def __telegram_message_text_start(self) -> str:
        return self.bot_text_messages.message_text_start()

    def __telegram_message_text_help(self) -> str:
        return self.bot_text_messages.message_text_help()

    def __telegram_message_text_subscribe(self, username_group: str) -> str:
        return self.bot_text_messages.message_subscribe(username_group)

    def __telegram_message_text_unsubscribe(self, username_group: str) -> str:
        return self.bot_text_messages.message_unsubscribe(username_group)

    def __telegram_message_text_theme_selection(self, theme: str) -> str:
        return self.bot_text_messages.message_theme(theme)
