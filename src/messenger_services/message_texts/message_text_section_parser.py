from abc import ABCMeta, abstractmethod

from data.html_parser import Element
from data.vector import List
from .message_text_section import MessageTextSection


class MessageTextSectionParser(metaclass=ABCMeta):
    @abstractmethod
    def get_message_text_elements(self, section: MessageTextSection) -> dict[str, List[Element]]: ...
