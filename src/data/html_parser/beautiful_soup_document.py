from functools import cached_property
from bs4 import (
    BeautifulSoup,
)

from data.vector import List
from .beautiful_soup_element_container import BeautifulSoupElementContainer
from .document import Document
from .element import Element


class BeautifulSoupDocument(Document, BeautifulSoupElementContainer):
    def __init__(self, html: str) -> None:
        soup = BeautifulSoup(html, 'lxml')
        super().__init__(soup)

    @cached_property
    def children(self) -> List[Element]:
        body = self.select('body').get_or_raise()
        return body.children
