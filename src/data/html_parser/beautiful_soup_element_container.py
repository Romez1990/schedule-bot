from abc import ABCMeta
from bs4.element import (
    Tag as BSElement,
    NavigableString,
)

from data.vector import List
from .element_container import ElementContainer
from .tag_element import TagElement
from .element import Element
from .beautiful_soup_text_element import BeautifulSoupTextElement


class BeautifulSoupElementContainer(ElementContainer, metaclass=ABCMeta):
    def __init__(self, container: BSElement) -> None:
        self.__container = container

    def select(self, selector: str) -> TagElement:
        element = self.__container.select_one(selector)
        return self.__create_beautiful_soup_tag_element(element)

    def select_all(self, selector: str) -> List[TagElement]:
        return List(self.__container.select(selector)) \
            .map(self.__create_beautiful_soup_tag_element)

    def __create_beautiful_soup_tag_element(self, element: BSElement) -> TagElement:
        from .beautiful_soup_tag_element import BeautifulSoupTagElement

        return BeautifulSoupTagElement(element)

    def _create_beautiful_soup_element(self, element: BSElement) -> Element:
        if isinstance(element, NavigableString):
            return BeautifulSoupTextElement(element)

        from .beautiful_soup_tag_element import BeautifulSoupTagElement

        return BeautifulSoupTagElement(element)
