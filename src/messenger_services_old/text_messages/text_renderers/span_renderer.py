from ..primitives import TextSpan


class SpanRenderer:
    def render(self, span: TextSpan) -> str:
        raise NotImplementedError
