from src.ioc_container import Module, Container
from .theme_repository_interface import ThemeRepositoryInterface
from .theme_repository import ThemeRepository


class ThemesModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(ThemeRepository).to(ThemeRepositoryInterface)
