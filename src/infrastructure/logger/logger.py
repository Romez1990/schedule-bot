from abc import ABCMeta, abstractmethod


class Logger(metaclass=ABCMeta):
    @abstractmethod
    def error(self, data: object) -> None: ...

    @abstractmethod
    def warning(self, data: object) -> None: ...

    @abstractmethod
    def info(self, data: object) -> None: ...

    @abstractmethod
    def debug(self, data: object) -> None: ...
