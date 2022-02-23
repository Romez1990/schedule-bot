from typing import (
    Callable,
    Type,
    TypeVar,
)

T = TypeVar('T')


def cast(new_type: Type[T]) -> Callable[[object], T]:
    def mapper(value: object) -> T:
        try:
            correct_type = isinstance(value, new_type)
        except TypeError as e:
            if str(e) != 'isinstance() argument 2 cannot be a parameterized generic':
                raise e
            correct_type = True

        if not correct_type:
            raise TypeError
        return value

    return mapper
