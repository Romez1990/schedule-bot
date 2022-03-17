from typing import (
    Callable,
    Sequence,
)
from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.task import async_identity
from data.serializers import BytesSerializerImpl
from data.hashing import Md5HashingImpl
from schedule_services.schedule import (
    Schedule,
    Group,
)
from schedule_services.update_checker import (
    UpdateCheckerImpl,
    ScheduleFetcherFactory,
    ScheduleFetcher,
)


@fixture(autouse=True)
def setup() -> None:
    global update_checker, schedule_fetcher, bytes_serializer, md5_hashing, on_schedules_changed
    schedule_fetcher = Mock()
    schedule_fetcher_factory: ScheduleFetcherFactory = Mock()

    def create_schedule_fetcher(on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> ScheduleFetcher:
        global schedules_fetched
        schedules_fetched = on_schedules_fetched
        return schedule_fetcher

    schedule_fetcher_factory.create = create_schedule_fetcher
    bytes_serializer = BytesSerializerImpl()
    md5_hashing = Md5HashingImpl()
    on_schedules_changed = Mock()
    update_checker = UpdateCheckerImpl(schedule_fetcher_factory, bytes_serializer, md5_hashing, on_schedules_changed)


update_checker: UpdateCheckerImpl
schedules_fetched: Callable[[Sequence[Schedule]], None]
schedule_fetcher: ScheduleFetcher
bytes_serializer: BytesSerializerImpl
md5_hashing: Md5HashingImpl
on_schedules_changed: Callable[[Schedule, list[Group]], None]


@mark.asyncio
async def test_start__calls_schedule_fetcher_start() -> None:
    schedule_fetcher.start = Mock(return_value=async_identity(None))

    await update_checker.start()

    schedule_fetcher.start.assert_called_once_with()
