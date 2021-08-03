from abc import ABCMeta, abstractmethod


class TextComponent(metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> str: ...
