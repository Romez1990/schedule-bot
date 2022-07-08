from typing import (
    Type,
    TypeVar,
)

from infrastructure.decorator import (
    check_decorating_class,
    check_decorating_class_name,
)
from .script_runner import ScriptRunner
from .base_script import ScriptBase

T = TypeVar('T', bound=ScriptBase)


def script(class_type: Type[T]) -> Type[T]:
    check_decorating_class(script, ScriptBase, class_type)
    check_decorating_class_name(class_type, 'Script')

    script_runner = ScriptRunner()
    script_runner.run(class_type)

    return class_type
