from data.html_parser import (
    Element,
)
from data.vector import List
from .components import TextComponentFactory
from .message_text_renderer import MessageTextRenderer
from .message_text_section import MessageTextSection


class MessageTextRendererImpl(MessageTextRenderer):
    def __init__(self, text_component_factory: TextComponentFactory) -> None:
        self.__text_component_factory = text_component_factory

    def parse_message_text_elements(self, section: MessageTextSection, message_text_name: str,
                                    elements: List[Element]) -> None:
        pass
