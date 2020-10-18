from returns.maybe import Maybe

from .theme import Theme


class ThemeRepositoryInterface:
    def get_by_name(self, name: str) -> Maybe[Theme]:
        raise NotImplementedError
