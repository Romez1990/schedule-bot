from abc import ABCMeta, abstractmethod

from .repository_connection import RepositoryConnection


class ManageableRepositoryConnection(RepositoryConnection, metaclass=ABCMeta):
    @abstractmethod
    def release(self) -> None: ...
