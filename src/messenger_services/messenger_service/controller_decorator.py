from typing import (
    Type,
    TypeVar,
)

from infrastructure.decorator import (
    check_decorating_class,
    check_decorating_class_name,
)
from .messenger_controller import MessengerController

messenger_controllers: list[Type[MessengerController]] = []

T = TypeVar('T', bound=MessengerController)


def controller(class_type: Type[T]) -> Type[T]:
    check_decorating_class(controller, MessengerController, class_type)
    check_decorating_class_name(class_type, 'Controller')
    messenger_controllers.append(class_type)
    return class_type
