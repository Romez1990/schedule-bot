from typing import (
    Iterable,
    Collection,
)

from .text_component import TextComponent
from .text_span import TextSpan


class Paragraph(TextComponent):
    def __init__(self, spans: Collection[TextSpan]) -> None:
        if len(spans) == 0:
            raise ValueError('paragraphs are empty')
        self.__spans = spans

    @property
    def children(self) -> Iterable[TextComponent]:
        return self.__spans
