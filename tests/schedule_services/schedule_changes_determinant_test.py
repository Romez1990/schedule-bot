from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.maybe import Nothing
from data.fp.task import Task
from schedule_services.update_checker import (
    ScheduleChangesDeterminantImpl,
    ScheduleHashing,
    ScheduleHashStorage,
)
from tests.schedule_services.schedules import schedule


@fixture(autouse=True)
def setup() -> None:
    global schedule_changes_determinant, schedule_hashing, schedule_hash_storage
    schedule_hashing = Mock()
    schedule_hash_storage = Mock()
    schedule_changes_determinant = ScheduleChangesDeterminantImpl(schedule_hashing, schedule_hash_storage)


schedule_changes_determinant: ScheduleChangesDeterminantImpl
schedule_hashing: ScheduleHashing
schedule_hash_storage: ScheduleHashStorage


@mark.asyncio
async def test_schedule_fetched__saves_hash_to_storage__when_no_hash_found_in_storage() -> None:
    schedules = [schedule]
    schedule_hash = 123
    schedule_hashing.hash = Mock(return_value=schedule_hash)
    schedule_hash_storage.get_hashes_by_dates = Mock(return_value=Task.from_value([Nothing]))
    schedule_hash_storage.save = Mock(return_value=Task.from_value(None))

    changed_schedules = await schedule_changes_determinant.get_changed_schedules(schedules)

    assert changed_schedules == schedules
    schedule_hashing.hash.assert_called_once_with(schedule)
    schedule_hash_storage.get_hashes_by_dates.assert_called_once_with([schedule.starts_at])
    schedule_hash_storage.save.assert_called_once_with([(schedule.starts_at, schedule_hash)])
