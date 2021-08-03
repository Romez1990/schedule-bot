from __future__ import annotations
from abc import ABCMeta, abstractmethod

from data.fp.maybe import Maybe
from .element import Element
from .element_container import ElementContainer


class TagElement(Element, ElementContainer, metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def get_attribute(self, attribute_name: str) -> Maybe[str]: ...

    @abstractmethod
    def children_to_html(self) -> str: ...
