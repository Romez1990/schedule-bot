from abc import ABCMeta, abstractmethod


class Md5ObjectHashing(metaclass=ABCMeta):
    @abstractmethod
    def hash(self, value: object) -> int: ...
