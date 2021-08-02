from typing import (
    Callable,
)


class DecoratorRegistrationError(Exception):
    def __init__(self, decorator: Callable, target: type, applying_object: object) -> None:
        super().__init__(f'"{decorator.__name__}" decorator can only be applied to "{target.__name__}", '
                         f'not to "{applying_object}"')
