from abc import ABCMeta, abstractmethod


class HttpClient(metaclass=ABCMeta):
    @abstractmethod
    def html(self, url: str) -> str: ...
