from src.ioc_container import Module, Container
from .schedule_renderer_interface import ScheduleRendererInterface
from .schedule_renderer import ScheduleRenderer


class RendererModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(ScheduleRenderer).to(ScheduleRendererInterface)
