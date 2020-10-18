from .text_renderers import TextRendererInterface
from .text_messages_interface import TextMessagesInterface
from .messages_interface import MessagesInterface


class TextMessages(TextMessagesInterface):
    def __init__(self, messages: MessagesInterface, text_renderer: TextRendererInterface) -> None:
        self.__messages = messages
        self.__text_renderer = text_renderer
        self.start = text_renderer.render(messages.start)
        self.help = text_renderer.render(messages.help)

    def subscribe(self, group_name: str) -> str:
        return self.__text_renderer.render(self.__messages.subscribe(group_name))

    def unsubscribe(self, group_name: str) -> str:
        return self.__text_renderer.render(self.__messages.unsubscribe(group_name))

    def change_theme(self, theme: str) -> str:
        return self.__text_renderer.render(self.__messages.change_theme(theme))
