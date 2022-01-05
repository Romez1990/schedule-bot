from abc import ABCMeta, abstractmethod


class CallerModuleNameRetriever(metaclass=ABCMeta):
    @abstractmethod
    def get_caller(self, stack_offset: int = 0): ...
