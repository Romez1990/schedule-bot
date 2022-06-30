from pytest import (
    raises,
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.task import Task
from schedule_services.schedule import Group
from schedule_services.scraper import ScheduleScraper
from schedule_services.update_checker import (
    ScheduleUpdateCheckerImpl,
    FetchInterval,
    ScheduleChangesDeterminant,
    WeekScheduleChangesDeterminant,
)
from tests.schedule_services.update_checker.schedules import schedule


@fixture(autouse=True)
def setup() -> None:
    global schedule_update_service, schedule_scraper, fetch_interval, schedule_changes_determinant, \
        week_schedule_changes_determinant
    schedule_scraper = Mock()
    fetch_interval = Mock()
    schedule_changes_determinant = Mock()
    week_schedule_changes_determinant = Mock()
    schedule_update_service = ScheduleUpdateCheckerImpl(schedule_scraper, fetch_interval, schedule_changes_determinant,
                                                        week_schedule_changes_determinant)


schedule_update_service: ScheduleUpdateCheckerImpl
schedule_scraper: ScheduleScraper
fetch_interval: FetchInterval
schedule_changes_determinant: ScheduleChangesDeterminant
week_schedule_changes_determinant: WeekScheduleChangesDeterminant


@mark.asyncio
async def test_get_schedules__raises_error__when_init_is_not_called() -> None:
    with raises(RuntimeError):
        schedule_update_service.get_schedules()


@mark.asyncio
async def test_init__() -> None:
    schedules_1 = [schedule]
    schedules_2 = [schedule]
    schedules_3 = [(schedule, [Group('ИС-20-Д')])]
    schedule_changes_determinant.init = Mock(return_value=Task.from_value(None))
    week_schedule_changes_determinant.init = Mock(return_value=Task.from_value(None))
    schedule_scraper.scrap_schedules = Mock(return_value=Task.from_value(schedules_1))
    schedule_changes_determinant.get_changed_schedules = Mock(return_value=Task.from_value(schedules_2))
    week_schedule_changes_determinant.get_changed_groups = Mock(return_value=Task.from_value(schedules_3))

    await schedule_update_service.init()
    result_schedules = schedule_update_service.get_schedules()

    schedule_changes_determinant.init.assert_called_once_with()
    week_schedule_changes_determinant.init.assert_called_once_with()
    schedule_scraper.scrap_schedules.assert_called_once_with()
    assert result_schedules is schedules_1
    schedule_changes_determinant.get_changed_schedules.assert_called_once_with(schedules_1)
    week_schedule_changes_determinant.get_changed_groups.assert_called_once_with(schedules_2)
