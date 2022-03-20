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
from data.fp.task import Task
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
    ScheduleUpdateServiceImpl,
    ScheduleFetcher,
    UpdateCheckerFactory,
)


@fixture(autouse=True)
def setup() -> None:
    global schedule_fetcher, update_checker_factory, schedule_update_service
    schedule_fetcher = Mock()
    update_checker_factory = Mock()
    schedule_update_service = ScheduleUpdateServiceImpl(schedule_fetcher, update_checker_factory)


schedule_fetcher: ScheduleFetcher
update_checker_factory: UpdateCheckerFactory
schedule_update_service: ScheduleUpdateServiceImpl


@mark.asyncio
async def test_start__starts_schedule_fetcher() -> None:
    schedule_fetcher.start = Mock(return_value=Task.from_value(None))

    await schedule_update_service.start_checking_updates()

    schedule_fetcher.start.assert_called_once_with()
