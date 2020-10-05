from .block import Block
from .color import Color


class Strip(Block):
    def __init__(self, x_pos: int, y_pos, width: int, height: int, color: Color) -> None:
        super().__init__(x_pos, y_pos, width, height)
        self.__color = color

    @property
    def color(self) -> Color:
        return self.__color
