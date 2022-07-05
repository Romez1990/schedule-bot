from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class GroupScheduleHash:
    starts_at: date
    group: str
    hash: int
    id: int | None = None

    def set_id(self, schedule_hash_id: int) -> GroupScheduleHash:
        return GroupScheduleHash(self.starts_at, self.group, self.hash, schedule_hash_id)

    def set_hash(self, hash: int) -> GroupScheduleHash:
        return GroupScheduleHash(self.starts_at, self.group, hash, self.id)
