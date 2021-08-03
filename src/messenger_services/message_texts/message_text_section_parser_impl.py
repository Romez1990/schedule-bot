from typing import (
    NoReturn, )

from data.html_parser import (
    HtmlParser,
    Element,
    TagElement,
    TextElement,
)
from data.vector import List
from .message_text_section import MessageTextSection
from .message_text_section_parser import MessageTextSectionParser


class MessageTextSectionParserImpl(MessageTextSectionParser):
    def __init__(self, html_parser: HtmlParser) -> None:
        self.__html_parser = html_parser

    __section: MessageTextSection

    def get_message_text_elements(self, section: MessageTextSection) -> dict[str, List[Element]]:
        self.__section = section
        document = self.__html_parser.parse(self.__section.content)
        message_text_elements = document.children \
            .refine(TagElement, self.__is_message_text_element)
        return {self.__get_message_text_name(element): self.__get_message_text(element)
                for element in message_text_elements}

    def __is_message_text_element(self, element: Element) -> bool:
        if isinstance(element, TextElement):
            if not element.text.isspace():
                raise Exception(f'in section {self.__section.name} there must be no text outside div blocks')
            return False
        return True

    def __get_message_text_name(self, element: TagElement) -> str:
        if element.name != 'div':
            raise Exception(f'in section {self.__section.name} message text element must be div element')

        def raise_no_name_error() -> NoReturn:
            raise Exception(f'in section {self.__section.name} no id attribute for message text div')

        return element.get_attribute('id').get_or_call(raise_no_name_error)

    def __get_message_text(self, element: TagElement) -> List[Element]:
        return element.children
