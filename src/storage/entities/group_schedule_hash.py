from __future__ import annotations
from datetime import date

from .entity_base import Entity


class GroupScheduleHash(Entity):
    def __init__(self, starts_at: date, group: str, hash: int, id: int = None) -> None:
        self.id = id
        self.starts_at = starts_at
        self.group = group
        self.hash = hash

    def set_id(self, schedule_hash_id: int) -> GroupScheduleHash:
        return GroupScheduleHash(self.starts_at, self.group, self.hash, schedule_hash_id)

    def set_hash(self, hash: int) -> GroupScheduleHash:
        return GroupScheduleHash(self.starts_at, self.group, hash, self.id)
