from platform_services.text_messages.text_messages_interface import TextMessagesInterface


class TextMessagesFactoryInterface:
    def create_plain_text_messages(self) -> TextMessagesInterface:
        raise NotImplementedError

    def create_html_text_messages(self) -> TextMessagesInterface:
        raise NotImplementedError
