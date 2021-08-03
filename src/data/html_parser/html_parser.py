from abc import ABCMeta, abstractmethod

from .document import Document


class HtmlParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, html: str) -> Document: ...
