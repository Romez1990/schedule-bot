from ..primitives import TextComponent


class TextRendererInterface:
    def render(self, component: TextComponent) -> str:
        raise NotImplementedError
