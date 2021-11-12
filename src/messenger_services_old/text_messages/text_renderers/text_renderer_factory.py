from .text_renderer_factory_interface import TextRendererFactoryInterface
from .text_renderer_interface import TextRendererInterface
from .text_renderer import TextRenderer
from .html_span_renderer import HtmlSpanRenderer
from .plain_text_span_renderer import PlainTextSpanRenderer


class TextRendererFactory(TextRendererFactoryInterface):
    def create_plain_text_renderer(self) -> TextRendererInterface:
        plain_text_span_renderer = PlainTextSpanRenderer()
        return TextRenderer(plain_text_span_renderer)

    def create_html_renderer(self) -> TextRendererInterface:
        html_span_renderer = HtmlSpanRenderer()
        return TextRenderer(html_span_renderer)
