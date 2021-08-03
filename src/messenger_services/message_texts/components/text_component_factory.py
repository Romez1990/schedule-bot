from abc import ABCMeta, abstractmethod

from data.vector import List
from .multi_paragraph_text import MultiParagraphText
from .paragraph import Paragraph
from .span import Span
from .font_style import FontStyle


class TextComponentFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_span(self, text: str, font_style: FontStyle) -> Span: ...

    @abstractmethod
    def create_paragraph(self, spans: List[Span]) -> Paragraph: ...

    @abstractmethod
    def create_multi_paragraph_text(self, paragraphs: List[Paragraph]) -> MultiParagraphText: ...
