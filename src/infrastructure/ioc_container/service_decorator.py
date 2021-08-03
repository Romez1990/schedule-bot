from typing import (
    Optional,
    Union,
    Callable,
    Type,
    TypeVar,
    cast,
)

from infrastructure.decorator import (
    check_decorating_type,
)
from .service_bind_parameters import ServiceBindParameters

services: list[ServiceBindParameters] = []

T = TypeVar('T')


def add_service(class_type: Type[T], to_self: Optional[bool] = None) -> Type[T]:
    check_decorating_type(service, object, class_type)
    services.append(ServiceBindParameters(class_type, to_self))
    return class_type


def service(to_self: bool) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    if isinstance(to_self, bool):
        def add_service_with_parameters(class_type: Type[T]) -> Type[T]:
            return add_service(class_type, to_self)

        return add_service_with_parameters
    return add_service(cast(Type[T], to_self))