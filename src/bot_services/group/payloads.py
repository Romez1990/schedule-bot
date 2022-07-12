from dataclasses import dataclass
from typing import (
    ClassVar,
)

from messenger_services.messenger_service import (
    Payload,
)


@dataclass(frozen=True, eq=False)
class SelectCoursePayload(Payload):
    type: ClassVar[str] = 'select_course'
    course: int


@dataclass(frozen=True, eq=False)
class AddGroupPayload(Payload):
    type: ClassVar[str] = 'add_group'
    group: str


@dataclass(frozen=True, eq=False)
class DeleteGroupPayload(Payload):
    type: ClassVar[str] = 'delete_group'
    group: str
