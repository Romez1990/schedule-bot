from data.vector import List
from messenger_services.message_texts.components import (
    MultiParagraphText,
    Paragraph,
)
from .separator_text_component import SeparatorTextComponent


class PlainMultiParagraphText(MultiParagraphText, SeparatorTextComponent):
    def __init__(self, paragraphs: List[Paragraph]) -> None:
        super().__init__(paragraphs, '\n')
