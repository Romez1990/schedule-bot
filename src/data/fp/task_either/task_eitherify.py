from typing import (
    Awaitable,
    Callable,
    TypeVar,
)

from data.fp.either import Either
from .task_either import TaskEither

L = TypeVar('L')
R = TypeVar('R')


def task_eitherify(fn: Callable[[...], Awaitable[Either[L, R]]]) -> Callable[[...], TaskEither[L, R]]:  # type: ignore
    def wrapper(*args: object, **kwargs: object) -> TaskEither[L, R]:
        return TaskEither(fn(*args, **kwargs))  # type: ignore

    return wrapper
