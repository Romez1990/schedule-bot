from data.vector import List
from messenger_services.message_texts.components import (
    Paragraph,
    Span,
)
from .separator_text_component import SeparatorTextComponent


class PlainParagraph(Paragraph, SeparatorTextComponent):
    def __init__(self, spans: List[Span]) -> None:
        super().__init__(spans, '')
