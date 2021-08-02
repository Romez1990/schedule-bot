from typing import (
    Callable,
)

from .decorator_registration_error import DecoratorRegistrationError
from .decorating_class_name_error import DecoratingClassNameError


def check_decorating_type(decorator: Callable, target: type, applying_object: type) -> None:
    if not issubclass(applying_object, target):
        raise DecoratorRegistrationError(decorator, target, applying_object)


def check_decorating_callable(decorator: Callable, function: object) -> None:
    if not callable(function):
        raise DecoratorRegistrationError(decorator, callable, function)


def check_decorating_class_name(class_type: type, suffix: str) -> None:
    if not class_type.__name__.endswith(suffix):
        raise DecoratingClassNameError(class_type, suffix)
