from typing import (
    Iterable,
    Collection,
)

from .text_component import TextComponent
from .paragraph import Paragraph


class Message(TextComponent):
    def __init__(self, paragraphs: Collection[Paragraph]) -> None:
        if len(paragraphs) == 0:
            raise ValueError('paragraphs are empty')
        self.__paragraphs = paragraphs

    @property
    def children(self) -> Iterable[TextComponent]:
        return self.__paragraphs
