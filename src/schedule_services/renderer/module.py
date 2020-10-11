from src.ioc_container import Module, ContainerBuilder
from .schedule_renderer_interface import ScheduleRendererInterface
from .schedule_renderer import ScheduleRenderer


class RendererModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(ScheduleRenderer).to(ScheduleRendererInterface)
