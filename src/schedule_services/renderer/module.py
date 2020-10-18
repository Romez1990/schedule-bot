from src.ioc_container import Module, Container
from .themes import ThemesModule
from .schedule_renderer_interface import ScheduleRendererInterface
from .schedule_renderer import ScheduleRenderer


class RendererModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(ThemesModule)
        container.bind(ScheduleRenderer).to(ScheduleRendererInterface)
