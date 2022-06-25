from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.task import Task
from schedule_services.scraper import ScheduleScraper
from schedule_services.update_checker import (
    UpdateCheckerImpl,
    FetchInterval,
    ScheduleChangesDeterminant,
    WeekScheduleChangesDeterminant,
)


@fixture(autouse=True)
def setup() -> None:
    global schedule_update_service, schedule_scraper, fetch_interval, schedule_changes_determinant, \
        week_schedule_changes_determinant
    schedule_scraper = Mock()
    fetch_interval = Mock()
    schedule_changes_determinant = Mock()
    week_schedule_changes_determinant = Mock()
    schedule_update_service = UpdateCheckerImpl(schedule_scraper, fetch_interval, schedule_changes_determinant,
                                                week_schedule_changes_determinant)


schedule_update_service: UpdateCheckerImpl
schedule_scraper: ScheduleScraper
fetch_interval: FetchInterval
schedule_changes_determinant: ScheduleChangesDeterminant
week_schedule_changes_determinant: WeekScheduleChangesDeterminant


# @mark.asyncio
# async def test_start__starts_schedule_fetcher() -> None:
#     fetch_interval.start = Mock(return_value=Task.from_value(None))
#
#     await schedule_update_service.start_checking_for_updates()
