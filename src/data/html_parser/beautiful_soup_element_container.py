from abc import ABCMeta
from bs4.element import (
    Tag as BSElement,
    NavigableString,
)

from data.fp.maybe import Maybe
from data.vector import List
from .element_container import ElementContainer
from .tag_element import TagElement
from .element import Element
from .beautiful_soup_text_element import BeautifulSoupTextElement


class BeautifulSoupElementContainer(ElementContainer, metaclass=ABCMeta):
    def __init__(self, element: BSElement) -> None:
        self._element = element

    def select(self, selector: str) -> Maybe[TagElement]:
        return Maybe.from_optional(self._element.select_one(selector)) \
            .map(self.__create_beautiful_soup_tag_element)

    def select_all(self, selector: str) -> List[TagElement]:
        return List(self._element.select(selector)) \
            .map(self.__create_beautiful_soup_tag_element)

    def __create_beautiful_soup_tag_element(self, element: BSElement) -> TagElement:
        from .beautiful_soup_tag_element import BeautifulSoupTagElement

        return BeautifulSoupTagElement(element)

    def _create_beautiful_soup_element(self, element: BSElement) -> Element:
        if isinstance(element, NavigableString):
            return BeautifulSoupTextElement(element)

        from .beautiful_soup_tag_element import BeautifulSoupTagElement

        return BeautifulSoupTagElement(element)

    def __str__(self) -> str:
        return str(self._element)
