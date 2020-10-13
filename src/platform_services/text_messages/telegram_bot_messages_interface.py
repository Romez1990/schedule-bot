class TelegramBotMessagesInterface:
    def __telegram_message_text_start(self) -> str:
        raise NotImplementedError

    def __telegram_message_text_help(self) -> str:
        raise NotImplementedError

    def __telegram_message_text_subscribe(self) -> str:
        raise NotImplementedError

    def __telegram_message_text_unsubscribe(self) -> str:
        raise NotImplementedError

    def __telegram_message_text_theme_selection(self) -> str:
        raise NotImplementedError