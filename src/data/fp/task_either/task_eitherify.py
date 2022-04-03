from typing import (
    Coroutine,
    Callable,
    TypeVar,
    ParamSpec,
)

from data.fp.either import Either
from .task_either import TaskEither

P = ParamSpec('P')
L = TypeVar('L')
R = TypeVar('R')


def task_eitherify(fn: Callable[P, Coroutine[object, None, Either[L, R]]]) -> Callable[P, TaskEither[L, R]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> TaskEither[L, R]:
        return TaskEither(fn(*args, **kwargs))
    return wrapper
