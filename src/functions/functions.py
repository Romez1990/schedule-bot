from typing import (
    Callable,
    TypeVar,
)

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')


def pipe2(arg: T1, function1: Callable[[T1], T2], function2: Callable[[T2], T3]) -> T3:
    return function2(function1(arg))
