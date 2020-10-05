from typing import (
    Union,
    List,
)
from bs4.element import (
    Tag as BSTag,
    NavigableString,
)

from .tag import Tag


class BeautifulSoupTag(Tag):
    def __init__(self, tag: BSTag) -> None:
        self.__tag = tag

    def select(self, selector: str) -> Tag:
        tag = self.__tag.select_one(selector)
        return self.__create_beautiful_soup_tag(tag)

    def select_all(self, selector: str) -> List[Tag]:
        tags = self.__tag.select(selector)
        return [self.__create_beautiful_soup_tag(tag) for tag in tags]

    def __create_beautiful_soup_tag(self, tag: BSTag) -> Tag:
        return BeautifulSoupTag(tag)

    @property
    def children(self) -> List[Union[Tag, str]]:
        return [self.__resolve_child(element) for element in self.__tag.contents]

    def __resolve_child(self, element: Union[BSTag, NavigableString]) -> Union[Tag, str]:
        if isinstance(element, BSTag):
            return BeautifulSoupTag(element)
        if isinstance(element, str):
            return str(element)
        raise ValueError(f'element is unexpected type {type(element).__name__}')

    @property
    def text(self) -> str:
        return self.__tag.get_text()

    def get_attribute(self, name: str) -> str:
        return self.__tag.attrs[name]
