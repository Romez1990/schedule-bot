from src.ioc_container import Module, Container
from .text_renderers import TextRenderersModule
from .text_messages_factory_interface import TextMessagesFactoryInterface
from .text_messages_factory import TextMessagesFactory
from .messages_interface import MessagesInterface
from .messages import Messages


class TextMessagesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(TextRenderersModule)
        container.bind(TextMessagesFactory).to(TextMessagesFactoryInterface)
        container.bind(Messages).to(MessagesInterface)
