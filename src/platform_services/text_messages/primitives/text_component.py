from __future__ import annotations
from typing import (
    Iterable,
)


class TextComponent:
    @property
    def children(self) -> Iterable[TextComponent]:
        raise NotImplementedError
