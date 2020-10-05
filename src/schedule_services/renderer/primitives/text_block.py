from .block import Block
from .alignment import Alignment
from .direction import Direction


class TextBlock(Block):
    def __init__(self, x_pos: int, y_pos, width: int, height: int, text: str, alignment=Alignment.center,
                 direction=Direction.horizontal) -> None:
        super().__init__(x_pos, y_pos, width, height)
        self.__text = text
        self.__alignment = alignment
        self.__direction = direction

    @property
    def text(self) -> str:
        return self.__text

    @property
    def alignment(self) -> Alignment:
        return self.__alignment

    @property
    def direction(self) -> Direction:
        return self.__direction
