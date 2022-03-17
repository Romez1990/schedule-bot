from abc import ABCMeta, abstractmethod


class Md5Hashing(metaclass=ABCMeta):
    @abstractmethod
    def hash(self, value: bytes) -> int: ...
