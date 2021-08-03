from abc import ABCMeta

from .text_component import TextComponent


class Paragraph(TextComponent, metaclass=ABCMeta):
    pass
