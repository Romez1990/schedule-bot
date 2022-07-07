from typing import (
    MutableSequence,
    Type,
    TypeVar,
)

from infrastructure.decorator import (
    check_decorating_type,
    check_decorating_class_name,
)
from .messenger_controller import MessengerController

messenger_controllers: MutableSequence[Type[MessengerController]] = []

T = TypeVar('T', bound=MessengerController)


def controller(class_type: Type[T]) -> Type[T]:
    check_decorating_type(controller, MessengerController, class_type)
    check_decorating_class_name(class_type, 'Controller')
    messenger_controllers.append(class_type)
    return class_type
