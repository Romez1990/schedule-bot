from abc import ABCMeta

from .text_component import TextComponent


class Span(TextComponent, metaclass=ABCMeta):
    pass
