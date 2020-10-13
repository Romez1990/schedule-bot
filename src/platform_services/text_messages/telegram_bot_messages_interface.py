class TelegramBotMessagesInterface:
    def __telegram_message_text_start(self):
        raise NotImplementedError

    def __telegram_message_text_help(self):
        raise NotImplementedError

    def __telegram_message_text_subscribe(self):
        raise NotImplementedError

    def __telegram_message_text_unsubscribe(self):
        raise NotImplementedError

    def __telegram_message_text_theme_selection(self):
        raise NotImplementedError
