from .text_component import TextComponent
from .font_type import FontType


class TextSpan(TextComponent):
    def __init__(self, text: str, font_type: FontType = FontType.normal) -> None:
        self.__text = text
        self.__font_type = font_type

    @property
    def text(self) -> str:
        return self.__text

    @property
    def font_type(self) -> FontType:
        return self.__font_type
