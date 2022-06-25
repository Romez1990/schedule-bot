from datetime import date
from unittest.mock import Mock

from pytest import (
    fixture,
    mark,
)

from data.fp.maybe import Some, Nothing
from data.fp.task import Task
from infrastructure.config import Config
from schedule_services.update_checker import (
    ScheduleHashStorageImpl,
)
from storage.entities import ScheduleHash
from storage.repositories import (
    ScheduleHashRepository,
)


@fixture(autouse=True)
def setup() -> None:
    global schedule_hash_storage, schedule_hash_repository, config
    schedule_hash_repository = Mock()
    config = Mock()
    schedule_hash_storage = ScheduleHashStorageImpl(schedule_hash_repository, config)


schedule_hash_storage: ScheduleHashStorageImpl
schedule_hash_repository: ScheduleHashRepository
config: Config


@mark.asyncio
async def test_init__calls_repository() -> None:
    schedule_hash_repository.get_all = Mock(return_value=Task.from_value([]))

    await schedule_hash_storage.init()

    schedule_hash_repository.get_all.assert_called_once_with()


@mark.asyncio
async def test_get_hashes_by_dates__returns_hash__when_repository_returns_it() -> None:
    schedule_hash_repository.get_all = Mock(return_value=Task.from_value([
        ScheduleHash(date(2022, 1, 1), 111),
    ]))

    await schedule_hash_storage.init()

    hashes = schedule_hash_storage.get_hashes_by_dates([date(2022, 1, 1)])
    assert hashes == [Some(111)]


@mark.asyncio
async def test_get_hashes_by_dates__does_not_return_hash__when_repository_does_not_return_it() -> None:
    schedule_hash_repository.get_all = Mock(return_value=Task.from_value([]))

    await schedule_hash_storage.init()

    hashes = schedule_hash_storage.get_hashes_by_dates([date(2022, 1, 1)])
    assert hashes == [Nothing]


@mark.asyncio
async def test_save__calls_repository_save_all__when_called_with_new_dates() -> None:
    schedule_hash_repository.save_all = Mock(side_effect=Task.from_value)
    config.weeks_to_store_schedule_hash = 999

    await schedule_hash_storage.save([
        (date(2022, 1, 1), 111),
        (date(2022, 2, 2), 222),
    ])

    hashes = schedule_hash_storage.get_hashes_by_dates([date(2022, 1, 1), date(2022, 2, 2)])
    assert hashes == [Some(111), Some(222)]
    schedule_hash_repository.save_all.assert_called_once_with([
        ScheduleHash(date(2022, 1, 1), 111),
        ScheduleHash(date(2022, 2, 2), 222),
    ])


@mark.asyncio
async def test_save__calls_repository_update_all__when_called_with_same_dates() -> None:
    schedule_hash_repository.save_all = Mock(side_effect=Task.from_value)
    schedule_hash_repository.update_all = Mock(return_value=Task.from_value(None))
    config.weeks_to_store_schedule_hash = 999
    await schedule_hash_storage.save([
        (date(2022, 1, 1), 111),
        (date(2022, 2, 2), 222),
    ])

    await schedule_hash_storage.save([
        (date(2022, 2, 2), 999),
        (date(2022, 3, 3), 333),
    ])

    hashes = schedule_hash_storage.get_hashes_by_dates([date(2022, 1, 1), date(2022, 2, 2), date(2022, 3, 3)])
    assert hashes == [Some(111), Some(999), Some(333)]
    schedule_hash_repository.save_all.assert_called_with([
        ScheduleHash(date(2022, 3, 3), 333),
    ])
    schedule_hash_repository.update_all.assert_called_once_with([
        ScheduleHash(date(2022, 2, 2), 999),
    ])


@mark.asyncio
async def test_save__calls_repository_delete_all__when_got_over_sized() -> None:
    schedule_hash_repository.save_all = Mock(side_effect=Task.from_value)
    schedule_hash_repository.update_all = Mock(return_value=Task.from_value(None))
    schedule_hash_repository.delete_all = Mock(return_value=Task.from_value(None))
    config.weeks_to_store_schedule_hash = 3
    await schedule_hash_storage.save([
        (date(2022, 1, 1), 111),
        (date(2022, 2, 2), 222),
        (date(2022, 3, 3), 333),
    ])

    await schedule_hash_storage.save([
        (date(2022, 3, 3), 999),
        (date(2022, 4, 4), 444),
        (date(2022, 5, 5), 555),
    ])

    hashes = schedule_hash_storage.get_hashes_by_dates([date(2022, 1, 1), date(2022, 2, 2), date(2022, 3, 3),
                                                        date(2022, 4, 4), date(2022, 5, 5)])
    assert hashes == [Nothing, Nothing, Some(999), Some(444), Some(555)]
    schedule_hash_repository.save_all.assert_called_with([
        ScheduleHash(date(2022, 4, 4), 444),
        ScheduleHash(date(2022, 5, 5), 555),
    ])
    schedule_hash_repository.update_all.assert_called_once_with([
        ScheduleHash(date(2022, 3, 3), 999),
    ])
    schedule_hash_repository.delete_all.assert_called_once_with([
        ScheduleHash(date(2022, 1, 1), 111),
        ScheduleHash(date(2022, 2, 2), 222),
    ])
