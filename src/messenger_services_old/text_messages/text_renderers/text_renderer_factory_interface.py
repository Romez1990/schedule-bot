from .text_renderer_interface import TextRendererInterface


class TextRendererFactoryInterface:
    def create_plain_text_renderer(self) -> TextRendererInterface:
        raise NotImplementedError

    def create_html_renderer(self) -> TextRendererInterface:
        raise NotImplementedError
