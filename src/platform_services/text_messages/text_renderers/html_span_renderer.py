from ..primitives import (
    TextSpan,
    FontType,
)
from .span_renderer import SpanRenderer


class HtmlSpanRenderer(SpanRenderer):
    def render(self, span: TextSpan) -> str:
        if span.font_type is FontType.bold:
            return f'<strong>{span.text}</strong>'
        if span.font_type is FontType.italic:
            return f'<em>{span.text}</em>'
        return span.text
