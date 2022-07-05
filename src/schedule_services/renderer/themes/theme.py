from dataclasses import dataclass
from typing import (
    Sequence,
)

from .color import Color


@dataclass(kw_only=True, frozen=True, eq=False)
class Theme:
    name: str
    text_color: Color
    background_colors: Sequence[Color]
