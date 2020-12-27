from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag as BSTag,
)

from .document import Document
from .tag import Tag
from .beautiful_soup_tag import BeautifulSoupTag


class BeautifulSoupDocument(Document):
    def __init__(self, html: str) -> None:
        self.__soup = BeautifulSoup(html, 'lxml')

    def select(self, selector: str) -> Tag:
        tag = self.__soup.select_one(selector)
        return self.__create_beautiful_soup_tag(tag)

    def select_all(self, selector: str) -> list[Tag]:
        tags = self.__soup.select(selector)
        return [self.__create_beautiful_soup_tag(tag) for tag in tags]

    def __create_beautiful_soup_tag(self, tag: BSTag) -> Tag:
        return BeautifulSoupTag(tag)
