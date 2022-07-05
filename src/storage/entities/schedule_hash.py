from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ScheduleHash:
    starts_at: date
    hash: int
    id: int | None = None

    def set_id(self, schedule_hash_id: int) -> ScheduleHash:
        return ScheduleHash(self.starts_at, self.hash, schedule_hash_id)

    def set_hash(self, hash: int) -> ScheduleHash:
        return ScheduleHash(self.starts_at, hash, self.id)
