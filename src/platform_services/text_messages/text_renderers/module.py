from src.ioc_container import Module, Container
from .text_renderer_factory_interface import TextRendererFactoryInterface
from .text_renderer_factory import TextRendererFactory
from .text_renderer_interface import TextRendererInterface
from .text_renderer import TextRenderer


class TextRenderersModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(TextRendererFactory).to(TextRendererFactoryInterface)
        container.bind(TextRenderer).to(TextRendererInterface)
