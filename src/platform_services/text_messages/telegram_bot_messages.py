from .telegram_bot_messages_interface import TelegramBotMessagesInterface
from .bot_text_messages import BotTextMessages


class TelegramBotMessages(TelegramBotMessagesInterface):
    def __init__(self, bot_text_messages: BotTextMessages) -> None:
        self.bot_text_messages = bot_text_messages

    def __telegram_message_text_start(self) -> str:
        return self.bot_text_messages.message_text_start()  # Argument and will need add to HTML parse mode for telegram

    def __telegram_message_text_help(self) -> str:
        return self.bot_text_messages.message_text_help()  # Argument and will need add to HTML parse mode for telegram

    def __telegram_message_text_subscribe(self) -> str:
        return self.bot_text_messages.message_subscribe()  # Argument and will need add to HTML parse mode for telegram

    def __telegram_message_text_unsubscribe(self) -> str:
        return self.bot_text_messages.message_unsubscribe()  # Argument and will need add to HTML parse mode for telegram

    def __telegram_message_text_theme_selection(self) -> str:
        return self.bot_text_messages.message_theme()  # Argument and will need add to HTML parse mode for telegram
