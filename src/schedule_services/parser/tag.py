from __future__ import annotations
from typing import (
    Union,
    List,
)


class Tag:
    def select(self, selector: str) -> Tag:
        raise NotImplementedError

    def select_all(self, selector: str) -> List[Tag]:
        raise NotImplementedError

    @property
    def children(self) -> List[Union[Tag, str]]:
        raise NotImplementedError

    @property
    def text(self) -> str:
        raise NotImplementedError

    def get_attribute(self, name: str) -> str:
        raise NotImplementedError
