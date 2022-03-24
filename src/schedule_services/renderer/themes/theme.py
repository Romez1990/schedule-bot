from typing import (
    Sequence,
)

from .color import Color


class Theme:
    def __init__(self, *, name: str, text_color: Color, background_colors: Sequence[Color]) -> None:
        self.name = name
        self.text_color = text_color
        self.background_colors = background_colors
