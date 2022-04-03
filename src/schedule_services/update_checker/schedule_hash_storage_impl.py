from datetime import date
from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.maybe import Maybe
from data.fp.task import Task
from storage.repositories import ScheduleHashRepository
from storage.entities import ScheduleHash
from .schedule_hash_storage import ScheduleHashStorage


@service
class ScheduleHashStorageImpl(ScheduleHashStorage):
    def __init__(self, schedule_hash_repository: ScheduleHashRepository) -> None:
        self.__schedule_hash_repository = schedule_hash_repository

    def get_hashes_by_dates(self, schedule_dates: Sequence[date]) -> Task[Sequence[Maybe[int]]]:
        pass

    def save(self, hashes: Sequence[tuple[date, int]]) -> Task[None]:
        pass
