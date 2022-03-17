from abc import ABCMeta, abstractmethod


class BytesSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, value: object) -> bytes: ...
