from abc import ABCMeta, abstractmethod

from .message_text_section import MessageTextSection


class MessageTextSectionReader(metaclass=ABCMeta):
    @abstractmethod
    def get_sections(self) -> dict[str, MessageTextSection]: ...
