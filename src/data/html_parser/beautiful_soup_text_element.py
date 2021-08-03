from bs4.element import (
    NavigableString,
)

from .text_element import TextElement


class BeautifulSoupTextElement(TextElement):
    def __init__(self, string: NavigableString) -> None:
        self.__string = string

    @property
    def text(self) -> str:
        return str(self.__string)

    def to_html(self) -> str:
        return str(self.__string)
