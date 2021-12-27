from abc import ABCMeta, abstractmethod

from data.fp.maybe import Maybe
from .theme import Theme


class ThemeRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_by_name(self, name: str) -> Maybe[Theme]: ...
