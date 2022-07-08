from typing import (
    MutableSequence,
    Union,
    Callable,
    Type,
    TypeVar,
    cast,
)

from infrastructure.decorator import (
    check_decorating_class,
)
from .service_bind_parameters import ServiceBindParameters

services: MutableSequence[ServiceBindParameters] = []
T = TypeVar('T')


def service(to_self: bool) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    if isinstance(to_self, bool):
        def add_service_with_parameters(class_type: Type[T]) -> Type[T]:
            return add_service(class_type, to_self)

        return add_service_with_parameters
    return add_service(cast(Type[T], to_self))


def add_service(class_type: Type[T], to_self: bool = None) -> Type[T]:
    check_decorating_class(service, object, class_type)
    services.append(ServiceBindParameters(class_type, to_self))
    return class_type
