from typing import (
    Awaitable,
    Callable,
    TypeVar,
)

from data.fp.maybe import Maybe
from .task_maybe import TaskMaybe

T = TypeVar('T')


def task_maybeify(fn: Callable[[...], Awaitable[Maybe[T]]]) -> Callable[[...], TaskMaybe[T]]:  # type: ignore
    def wrapper(*args: object, **kwargs: object) -> TaskMaybe[T]:
        return TaskMaybe(fn(*args, **kwargs))  # type: ignore

    return wrapper
