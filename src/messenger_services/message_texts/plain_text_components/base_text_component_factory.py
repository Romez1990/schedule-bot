from abc import ABCMeta

from data.vector import List
from messenger_services.message_texts.components import (
    TextComponentFactory,
    Paragraph,
    MultiParagraphText,
    Span,
)
from .multi_paragraph_text import PlainMultiParagraphText
from .paragraph import PlainParagraph


class BaseTextComponentFactory(TextComponentFactory, metaclass=ABCMeta):
    def create_paragraph(self, spans: List[Span]) -> Paragraph:
        return PlainParagraph(spans)

    def create_multi_paragraph_text(self, paragraphs: List[Paragraph]) -> MultiParagraphText:
        return PlainMultiParagraphText(paragraphs)
