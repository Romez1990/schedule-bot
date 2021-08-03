from messenger_services.message_texts.components import (
    Span,
)


class PlainSpan(Span):
    def __init__(self, text: str) -> None:
        self.__text = text

    def render(self) -> str:
        return self.__text
