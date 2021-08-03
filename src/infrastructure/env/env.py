from abc import ABCMeta, abstractmethod


class Env(metaclass=ABCMeta):
    @abstractmethod
    def get_str(self, var_name: str) -> str: ...

    @abstractmethod
    def get_bool(self, var_name: str) -> bool: ...

    @abstractmethod
    def get_int(self, var_name: str) -> int: ...

    @abstractmethod
    def get_positive_int(self, var_name: str) -> int: ...

    @abstractmethod
    def get_float(self, var_name: str) -> float: ...

    @abstractmethod
    def get_positive_float(self, var_name: str) -> float: ...
