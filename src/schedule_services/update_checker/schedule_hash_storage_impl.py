from datetime import date
from typing import Awaitable

from data.fp.maybe import Maybe
from data.fp.task import Task
from infrastructure.ioc_container import service
from .schedule_hash_storage import ScheduleHashStorage
from storage.repositories import ScheduleHashRepository


@service
class ScheduleHashStorageImpl(ScheduleHashStorage):
    def __init__(self, schedule_hash_repository: ScheduleHashRepository) -> None:
        self.__schedule_hash_repository = schedule_hash_repository

    def get_hash_by_date(self, schedule_date: date) -> Task[Maybe[int]]:
        pass

    async def save(self, schedule_date: date, schedule_hash: int) -> None:
        pass

    def update_schedule_hash(self, schedule_date: date, schedule_hash: int) -> Awaitable[None]:
        pass
