from __future__ import annotations
from datetime import date

from .entity_base import Entity


class ScheduleHash(Entity):
    def __init__(self, schedule_date: date, schedule_hash: int, schedule_hash_id: int = None) -> None:
        self.id = schedule_hash_id
        self.date = schedule_date
        self.hash = schedule_hash

    def set_id(self, schedule_hash_id: int) -> ScheduleHash:
        return ScheduleHash(self.date, self.hash, schedule_hash_id)
