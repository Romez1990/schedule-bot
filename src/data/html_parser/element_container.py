from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    TYPE_CHECKING,
)

from data.vector import List
from .element import Element

if TYPE_CHECKING:
    from .tag_element import TagElement


class ElementContainer(metaclass=ABCMeta):
    @property
    @abstractmethod
    def children(self) -> List[Element]: ...

    @abstractmethod
    def select(self, selector: str) -> TagElement: ...

    @abstractmethod
    def select_all(self, selector: str) -> List[TagElement]: ...
