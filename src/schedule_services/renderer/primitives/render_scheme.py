from typing import (
    Iterable,
)
from pyrsistent import pvector

from .strip import Strip
from .text_block import TextBlock


class RenderScheme:
    def __init__(self, width: int, height: int, strips: Iterable[Strip], text_blocks: Iterable[TextBlock]) -> None:
        self.__width = width
        self.__height = height
        self.__strips = pvector(strips)
        self.__text_blocks = pvector(text_blocks)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def strips(self) -> Iterable[Strip]:
        return self.__strips

    @property
    def text_blocks(self) -> Iterable[TextBlock]:
        return self.__text_blocks
