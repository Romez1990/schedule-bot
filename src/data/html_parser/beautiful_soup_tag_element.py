from functools import cached_property
from bs4.element import (
    Tag as BSElement,
)

from data.fp.maybe import Maybe
from data.vector import List
from .tag_element import TagElement
from .beautiful_soup_element_container import BeautifulSoupElementContainer
from .element import Element


class BeautifulSoupTagElement(TagElement, BeautifulSoupElementContainer):
    def __init__(self, element: BSElement) -> None:
        super().__init__(element)

    @property
    def text(self) -> str:
        return self._element.get_text()

    @property
    def name(self) -> str:
        return self._element.name

    @cached_property
    def children(self) -> List[Element]:
        return List(self._element.children) \
            .map(self._create_beautiful_soup_element)

    def get_attribute(self, attribute_name: str) -> Maybe[str]:
        def get_attribute() -> str:
            return self._element.attrs[attribute_name]
        return Maybe.try_except(get_attribute, KeyError)

    def to_html(self) -> str:
        return str(self._element)

    def children_to_html(self) -> str:
        html_of_elements = List(self._element.children) \
            .map(self.__element_to_html)
        return ''.join(html_of_elements)

    def __element_to_html(self, element: BSElement) -> str:
        return str(element)
