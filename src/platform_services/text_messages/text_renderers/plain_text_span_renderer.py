from ..primitives import (
    TextSpan,
)
from .span_renderer import SpanRenderer


class PlainTextSpanRenderer(SpanRenderer):
    def render(self, span: TextSpan) -> str:
        return span.text
