from typing import (
    Coroutine,
    Callable,
    TypeVar,
    ParamSpec,
)

from .task import Task

P = ParamSpec('P')
T = TypeVar('T')


def taskify(fn: Callable[P, Coroutine[object, None, T]]) -> Callable[P, Task[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Task[T]:
        return Task(fn(*args, **kwargs))

    return wrapper
