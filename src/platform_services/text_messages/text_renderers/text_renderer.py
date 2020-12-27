from src.immutable_collections import (
    List,
)
from ..primitives import (
    TextComponent,
    Message,
    Paragraph,
    TextSpan,
    FontType,
)
from .text_renderer_interface import TextRendererInterface
from .span_renderer import SpanRenderer


class TextRenderer(TextRendererInterface):
    def __init__(self, span_renderer: SpanRenderer) -> None:
        self.__span_renderer = span_renderer

    def render(self, component: TextComponent) -> str:
        if isinstance(component, Message):
            return self.__render_message(component)
        if isinstance(component, Paragraph):
            return self.__render_paragraph(component)
        if isinstance(component, TextSpan):
            return self.__span_renderer.render(component)
        raise NotImplemented

    def __render_message(self, message: Message) -> str:
        return List(message.children) \
            .map(self.render) \
            .reduce(self.__join_paragraphs)

    def __render_paragraph(self, paragraph: Paragraph) -> str:
        return List(paragraph.children) \
            .map(self.render) \
            .reduce(self.__join_spans)

    def __join_paragraphs(self, paragraph1: str, paragraph2: str) -> str:
        return paragraph1 + '\n' + paragraph2

    def __join_spans(self, span1: str, span2: str) -> str:
        return span1 + span2
