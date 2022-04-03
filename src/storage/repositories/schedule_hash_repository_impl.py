from datetime import date
from typing import (
    Sequence,
    Mapping,
    cast,
)

from infrastructure.ioc_container import service
from data.vector import List
from data.fp.task import taskify
from storage.database import Record
from storage.entities import ScheduleHash
from .repository_base import RepositoryBase
from .schedule_hash_repository import ScheduleHashRepository


@service
class ScheduleHashRepositoryImpl(ScheduleHashRepository, RepositoryBase):
    @taskify
    async def get_all(self) -> Sequence[ScheduleHash]:
        async with self._get_connection() as connection:
            records = await connection.fetch('''
                SELECT * FROM schedule_hashes
                ORDER BY starts_at
            ''')
        return List(records).map(self.__create_schedule_hash)

    def __create_schedule_hash(self, record: Record) -> ScheduleHash:
        return ScheduleHash(**record)

    @taskify
    async def save_all(self, schedule_hashes: Sequence[ScheduleHash]) -> Sequence[ScheduleHash]:
        data = List(schedule_hashes) \
            .map(self.__entity_to_tuple)
        async with self._get_connection() as connection:
            ids = await connection.fetch('''
                INSERT INTO schedule_hashes(starts_at, hash)
                (SELECT
                    r.starts_at, r.hash
                FROM
                    unnest($1::schedule_hashes[]) as r
                )
                RETURNING id
            ''', data)
        return List.zip(schedule_hashes, ids) \
            .map(self.__set_id)

    def __entity_to_tuple(self, schedule_hash: ScheduleHash) -> tuple[None, date, int]:
        return None, schedule_hash.starts_at, schedule_hash.hash

    def __set_id(self, t: tuple[ScheduleHash, Mapping[str, object]]) -> ScheduleHash:
        schedule_hash, id_record = t
        id = cast(int, id_record['id'])
        return schedule_hash.set_id(id)

    @taskify
    async def delete_all(self, schedule_hashes: Sequence[ScheduleHash]) -> None:
        ids = List(schedule_hashes).map(self.__get_id)
        async with self._get_connection() as connection:
            await connection.execute_many('''
                DELETE FROM schedule_hashes
                WHERE id = ($1)
            ''', list(ids))

    def __get_id(self, schedule_hash: ScheduleHash) -> tuple[int]:
        return schedule_hash.id,
