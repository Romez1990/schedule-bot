from abc import ABCMeta, abstractmethod

from data.fp.task_either import TaskEither


class HttpClient(metaclass=ABCMeta):
    @abstractmethod
    def html(self, url: str) -> TaskEither[Exception, str]: ...
