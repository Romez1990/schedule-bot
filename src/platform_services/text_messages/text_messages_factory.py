from .text_renderers import TextRendererFactoryInterface
from .text_messages_factory_interface import TextMessagesFactoryInterface
from .messages_interface import MessagesInterface
from .text_messages_interface import TextMessagesInterface
from .text_messages import TextMessages


class TextMessagesFactory(TextMessagesFactoryInterface):
    def __init__(self, messages: MessagesInterface, text_renderer_factory: TextRendererFactoryInterface) -> None:
        self.__messages = messages
        self.__text_renderer_factory = text_renderer_factory

    def create_plain_text_messages(self) -> TextMessagesInterface:
        return TextMessages(self.__messages, self.__text_renderer_factory.create_plain_text_renderer())

    def create_html_text_messages(self) -> TextMessagesInterface:
        return TextMessages(self.__messages, self.__text_renderer_factory.create_html_renderer())
