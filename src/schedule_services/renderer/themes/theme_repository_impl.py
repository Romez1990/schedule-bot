from typing import (
    Mapping,
)

from infrastructure.ioc_container import service
from data.fp.maybe import Maybe, Some, Nothing
from .theme_repository import ThemeRepository
from .theme import Theme
from .color import Color


@service
class ThemeRepositoryImpl(ThemeRepository):
    def __init__(self) -> None:
        themes = [
            Theme(
                name='light',
                text_color=Color(0, 0, 0),
                background_colors=[Color(255, 255, 255), Color(238, 238, 238)],
            ),
            Theme(
                name='dark',
                text_color=Color(173, 173, 173),
                background_colors=[Color(37, 37, 38), Color(32, 32, 33)],
            ),
        ]
        self.__themes: Mapping[str, Theme] = {theme.name: theme for theme in themes}

    def find_by_name(self, name: str) -> Maybe[Theme]:
        if name not in self.__themes:
            return Nothing
        return Some(self.__themes[name])
