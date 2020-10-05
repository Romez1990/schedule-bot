from src.ioc_container import Module, ContainerBuilder
from .parser import ParserModule
from .scraper import ScraperModule
from .renderer import RendererModule


class ScheduleServicesModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(ParserModule)
        builder.register_module(ScraperModule)
        builder.register_module(RendererModule)
