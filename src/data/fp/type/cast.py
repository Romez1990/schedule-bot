from typing import (
    Callable,
    Type,
    TypeVar,
)

T = TypeVar('T')


def cast(new_type: Type[T]) -> Callable[[object], T]:
    def mapper(value: object) -> T:
        if not isinstance(value, new_type):
            raise TypeError
        return value

    return mapper
