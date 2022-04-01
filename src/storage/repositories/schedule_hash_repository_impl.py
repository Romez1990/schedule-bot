from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.task import taskify
from storage.entities import ScheduleHash
from .repository_base import RepositoryBase
from .schedule_hash_repository import ScheduleHashRepository


@service
class ScheduleHashRepositoryImpl(ScheduleHashRepository, RepositoryBase):
    @taskify
    async def save_all(self, schedule_hashes: Sequence[ScheduleHash]) -> Sequence[ScheduleHash]:
        schedule_hash = schedule_hashes[0]
        async with self._get_connection() as connection:
            await connection.execute('''
                INSERT INTO schedule_hashes(starts_at, hash)
                VALUES ($1, $2)
            ''', schedule_hash.starts_at, schedule_hash.hash)
            id = await connection.fetch_value('''SELECT currval('schedule_hashes_id_seq')''', value_type=int)
            return [schedule_hash.set_id(id)]
