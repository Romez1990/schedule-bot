from __future__ import annotations
from datetime import date

from .entity_base import Entity


class ScheduleHash(Entity):
    def __init__(self, starts_at: date, hash: int, id: int = None) -> None:
        self.id = id
        self.starts_at = starts_at
        self.hash = hash

    def set_id(self, schedule_hash_id: int) -> ScheduleHash:
        return ScheduleHash(self.starts_at, self.hash, schedule_hash_id)
