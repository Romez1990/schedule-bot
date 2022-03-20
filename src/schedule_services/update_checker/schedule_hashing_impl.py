from infrastructure.ioc_container import service
from data.serializers import BytesSerializer
from data.hashing import Md5Hashing
from schedule_services.schedule import (
    Schedule,
    DaySchedule,
)
from .schedule_hashing import ScheduleHashing


@service
class ScheduleHashingImpl(ScheduleHashing):
    def __init__(self, bytes_serializer: BytesSerializer, md5_hashing: Md5Hashing) -> None:
        self.__bytes_serializer = bytes_serializer
        self.__md5_hashing = md5_hashing

    def hash(self, schedule: Schedule | DaySchedule) -> int:
        schedule_bytes = self.__bytes_serializer.serialize(schedule)
        return self.__md5_hashing.hash(schedule_bytes)
