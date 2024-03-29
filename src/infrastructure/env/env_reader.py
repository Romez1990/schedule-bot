from abc import ABCMeta, abstractmethod


class EnvReader(metaclass=ABCMeta):
    @abstractmethod
    def get_str(self, var_name: str) -> str | None: ...
