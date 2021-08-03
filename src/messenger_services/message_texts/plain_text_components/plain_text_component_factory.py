from messenger_services.message_texts.components import (
    Span,
    FontStyle,
)
from .base_text_component_factory import BaseTextComponentFactory
from .span import PlainSpan


class PlainTextComponentFactory(BaseTextComponentFactory):
    def create_span(self, text: str, font_style: FontStyle) -> Span:
        return PlainSpan(text)
