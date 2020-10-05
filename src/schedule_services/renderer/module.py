from src.ioc_container import Module, Container
from .themes import ThemesModule
from .schedule_renderer_interface import ScheduleRendererInterface
from .schedule_renderer import ScheduleRenderer
from .schedule_transformer_interface import ScheduleTransformerInterface
from .schedule_transformer import ScheduleTransformer
from .theme_repository_interface import ThemeRepositoryInterface
from .theme_repository import ThemeRepository


class RendererModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(ThemesModule)
        container.bind(ScheduleRenderer).to(ScheduleRendererInterface)
        container.bind(ScheduleTransformer).to(ScheduleTransformerInterface)
        container.bind(ThemeRepository).to(ThemeRepositoryInterface)
