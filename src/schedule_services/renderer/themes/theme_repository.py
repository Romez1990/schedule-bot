from returns.maybe import Maybe

from src.utilities import ListHelper
from .theme_repository_interface import ThemeRepositoryInterface
from .theme import Theme
from .color import Color


class ThemeRepository(ThemeRepositoryInterface):
    def __init__(self, list_helper: ListHelper) -> None:
        self.__list_helper = list_helper
        self.__themes = [
            Theme('light', Color(0, 0, 0), [Color(255, 255, 255), Color(238, 238, 238)]),
            Theme('dark', Color(173, 173, 173), [Color(37, 37, 38), Color(32, 32, 33)]),
        ]

    def get_by_name(self, name: str) -> Maybe[Theme]:
        return self.__list_helper.find_first(self.__themes, lambda theme: theme.name == name)
