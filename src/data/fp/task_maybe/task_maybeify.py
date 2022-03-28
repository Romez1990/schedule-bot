from typing import (
    Awaitable,
    Callable,
    TypeVar,
    ParamSpec,
)

from data.fp.maybe import Maybe
from .task_maybe import TaskMaybe

P = ParamSpec('P')
T = TypeVar('T')


def task_maybeify(fn: Callable[P, Awaitable[Maybe[T]]]) -> Callable[P, TaskMaybe[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> TaskMaybe[T]:
        return TaskMaybe(fn(*args, **kwargs))

    return wrapper
