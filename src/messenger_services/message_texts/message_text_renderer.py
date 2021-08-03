from abc import ABCMeta, abstractmethod

from data.html_parser import (
    Element,
)
from data.vector import List
from .message_text_section import MessageTextSection


class MessageTextRenderer(metaclass=ABCMeta):
    @abstractmethod
    def parse_message_text_elements(self, section: MessageTextSection, message_text_name: str,
                                    elements: List[Element]) -> None: ...
