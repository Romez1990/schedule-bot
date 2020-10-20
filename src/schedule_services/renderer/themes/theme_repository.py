from typing import (
    Mapping,
)
from returns.maybe import Maybe, Some, Nothing

from .theme_repository_interface import ThemeRepositoryInterface
from .theme import Theme
from .color import Color


class ThemeRepository(ThemeRepositoryInterface):
    def __init__(self) -> None:
        themes = [
            Theme('light', Color(0, 0, 0), [Color(255, 255, 255), Color(238, 238, 238)]),
            Theme('dark', Color(173, 173, 173), [Color(37, 37, 38), Color(32, 32, 33)]),
        ]
        self.__themes: Mapping[str, Theme] = {theme.name: theme for theme in themes}

    def get_by_name(self, name: str) -> Maybe[Theme]:
        if name not in self.__themes:
            return Nothing
        return Some(self.__themes[name])
