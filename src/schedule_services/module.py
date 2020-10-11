from src.ioc_container import Module, Container
from .parser import ParserModule
from .scraper import ScraperModule
from .renderer import RendererModule


class ScheduleServicesModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(ParserModule)
        container.register_module(ScraperModule)
        container.register_module(RendererModule)
