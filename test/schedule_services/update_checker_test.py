from datetime import date
from typing import (
    Callable,
    Sequence,
)
from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.maybe import Some, Nothing
from data.fp.task_maybe import TaskNothing
from data.serializers import BytesSerializerImpl
from schedule_services.schedule import (
    Schedule,
    Group,
    WeekSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from schedule_services.update_checker import (
    UpdateCheckerImpl,
    ScheduleFetcher,
    ScheduleHashing,
    ScheduleHashStorage,
)


@fixture(autouse=True)
def setup() -> None:
    global update_checker, schedule_fetcher, schedule_hashing, schedule_hash_storage, on_schedules_changed
    schedule_fetcher = Mock()

    def create_schedule_fetcher(on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> None:
        global schedules_fetched
        schedules_fetched = on_schedules_fetched

    schedule_fetcher.subscribe_for_updates = create_schedule_fetcher
    schedule_hashing = Mock()
    schedule_hash_storage = Mock()
    on_schedules_changed = Mock()
    update_checker = UpdateCheckerImpl(schedule_fetcher, schedule_hashing, schedule_hash_storage, on_schedules_changed)


update_checker: UpdateCheckerImpl
schedules_fetched: Callable[[Sequence[Schedule]], None]
schedule_fetcher: ScheduleFetcher
schedule_hashing: ScheduleHashing
schedule_hash_storage: ScheduleHashStorage
on_schedules_changed: Callable[[Schedule, list[Group]], None]


@mark.asyncio
async def test_schedule_fetched__saves_hash_to_storage__when_no_hash_found_in_storage() -> None:
    schedule_hash = 123
    schedule_hashing.hash = Mock(return_value=schedule_hash)
    schedule_hash_storage.get_hash_by_date = Mock(return_value=TaskNothing())
    schedule_hash_storage.save = Mock()

    schedules_fetched([schedule])

    schedule_hashing.hash.assert_called_once_with(schedule)
    schedule_hash_storage.get_hash_by_date.assert_called_once_with(schedule.week_start)
    schedule_hash_storage.save.assert_called_once_with(schedule.week_start, schedule_hash)


schedule = Schedule(date(2022, 3, 14), {
    Group('ИС-20-Д'): WeekSchedule(DayOfWeek.monday, [
        DaySchedule([
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
        ]),
        DaySchedule([
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
        ]),
        DaySchedule([
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
        ]),
        DaySchedule([
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
        ]),
        DaySchedule([
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
            Some(Entry('', '', '', '')),
        ]),
    ]),
})


def change_schedule() -> Schedule:
    serializer = BytesSerializerImpl()
    schedule_bytes = serializer.serialize(schedule)
    schedule_2 = serializer.deserialize(schedule_bytes, Schedule)
    group_schedule = schedule_2._data[Group('ИС-20-Д')]
    friday_schedule = group_schedule._WeekSchedule__day_schedules[-1]
    friday_entries = list(friday_schedule._DaySchedule__entries)
    friday_entries[0] = Nothing
    friday_schedule._DaySchedule__entries = tuple(friday_entries)
    return schedule_2


schedule_2 = change_schedule()
