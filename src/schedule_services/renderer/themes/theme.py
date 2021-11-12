from typing import (
    Sequence,
)

from .color import Color


class Theme:
    def __init__(self, name: str, text_color: Color, background_colors: Sequence[Color]) -> None:
        self.__name = name
        self.__background_colors = background_colors
        self.__text_color = text_color

    @property
    def name(self) -> str:
        return self.__name

    @property
    def text_color(self) -> Color:
        return self.__text_color

    @property
    def background_colors(self) -> Sequence[Color]:
        return self.__background_colors

    def get_nth_background_color(self, n: int) -> Color:
        background_color_index = n % len(self.__background_colors)
        return self.__background_colors[background_color_index]
