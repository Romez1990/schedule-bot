from typing import (
    MutableSequence,
    Type,
    TypeVar,
)

from infrastructure.decorator import (
    check_decorating_class,
    check_decorating_class_name,
)
from .migration import Migration

T = TypeVar('T', bound=Migration)

migrations: MutableSequence[Type[Migration]] = []


def migration(class_type: Type[T]) -> Type[T]:
    check_decorating_class(migration, Migration, class_type)
    check_decorating_class_name(class_type, Migration.__name__)
    migrations.append(class_type)
    return class_type
