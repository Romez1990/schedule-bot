from abc import ABCMeta

from .element_container import ElementContainer


class Document(ElementContainer, metaclass=ABCMeta):
    pass
