from abc import ABCMeta, abstractmethod


class Element(metaclass=ABCMeta):
    @property
    @abstractmethod
    def text(self) -> str: ...

    @abstractmethod
    def to_html(self) -> str: ...
