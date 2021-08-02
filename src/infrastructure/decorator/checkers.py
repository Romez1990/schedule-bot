from typing import (
    Callable,
)

from .decorator_registration_error import DecoratorRegistrationError


def check_decorating_type(decorator: Callable, target: type, applying_object: type) -> None:
    if not issubclass(applying_object, target):
        raise DecoratorRegistrationError(decorator, target, applying_object)
