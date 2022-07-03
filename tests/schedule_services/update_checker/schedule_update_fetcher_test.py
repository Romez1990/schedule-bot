from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.task import Task
from schedule_services.schedule import Group
from schedule_services.scraper import ScheduleScraper
from schedule_services.update_checker import (
    ScheduleUpdateFetcherImpl,
    ScheduleChangesDeterminant,
    WeekScheduleChangesDeterminant,
)
from tests.schedule_services.update_checker.schedules import (
    schedule,
    schedule_2,
)


@fixture(autouse=True)
def setup() -> None:
    global schedule_update_fetcher, schedule_scraper, schedule_changes_determinant, week_schedule_changes_determinant
    schedule_scraper = Mock()
    schedule_changes_determinant = Mock()
    week_schedule_changes_determinant = Mock()
    schedule_update_fetcher = ScheduleUpdateFetcherImpl(schedule_scraper, schedule_changes_determinant,
                                                        week_schedule_changes_determinant)


schedule_update_fetcher: ScheduleUpdateFetcherImpl
schedule_scraper: ScheduleScraper
schedule_changes_determinant: ScheduleChangesDeterminant
week_schedule_changes_determinant: WeekScheduleChangesDeterminant


@mark.asyncio
async def test_init__calls_init_of_determinants() -> None:
    schedule_changes_determinant.init = Mock(return_value=Task.from_value(None))
    week_schedule_changes_determinant.init = Mock(return_value=Task.from_value(None))

    await schedule_update_fetcher.init()

    schedule_changes_determinant.init.assert_called_once_with()
    week_schedule_changes_determinant.init.assert_called_once_with()


@mark.asyncio
async def test_fetch_updates() -> None:
    schedules_1 = [schedule, schedule_2]
    schedules_2 = [schedule]
    schedules_3 = [(schedule, [Group('ИС-20-Д')])]
    schedule_scraper.scrap_schedules = Mock(return_value=Task.from_value(schedules_1))
    schedule_changes_determinant.get_changed_schedules = Mock(return_value=Task.from_value(schedules_2))
    week_schedule_changes_determinant.get_changed_groups = Mock(return_value=Task.from_value(schedules_3))

    result = await schedule_update_fetcher.fetch_updates()

    schedule_scraper.scrap_schedules.assert_called_once_with()
    schedule_changes_determinant.get_changed_schedules.assert_called_once_with(schedules_1)
    week_schedule_changes_determinant.get_changed_groups.assert_called_once_with(schedules_2)
    assert result == (schedules_1, schedules_3)
