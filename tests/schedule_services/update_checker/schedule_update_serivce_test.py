from asyncio import (
    Future,
    create_task,
    sleep,
)
from pytest import (
    raises,
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.task import Task
from schedule_services.schedule import Group
from schedule_services.update_checker import (
    ScheduleUpdateServiceImpl,
    FetchInterval,
    ScheduleUpdateFetcher,
)
from tests.schedule_services.update_checker.schedules import (
    schedule,
)


@fixture(autouse=True)
def setup() -> None:
    global schedule_update_service, fetch_interval, schedule_update_fetcher
    schedule_update_fetcher = Mock()
    fetch_interval = Mock()
    schedule_update_service = ScheduleUpdateServiceImpl(schedule_update_fetcher, fetch_interval)


schedule_update_service: ScheduleUpdateServiceImpl
schedule_update_fetcher: ScheduleUpdateFetcher
fetch_interval: FetchInterval


@mark.asyncio
async def test_get_schedules__raises_error__when_init_is_not_called() -> None:
    with raises(RuntimeError):
        schedule_update_service.get_schedules()


@mark.asyncio
async def test_init__gets_schedules_and_calls_subscribers() -> None:
    schedules = [schedule]
    updates = [(schedule, [Group('ИС-20-Д')])]
    fetch_result = schedules, updates
    schedule_update_fetcher.init = Mock(return_value=Task.from_value(None))
    schedule_update_fetcher.fetch_updates = Mock(return_value=Task.from_value(fetch_result))
    subscriber_1 = Mock()
    subscriber_2 = Mock()

    schedule_update_service.subscribe_to_updates(subscriber_1)
    schedule_update_service.subscribe_to_updates(subscriber_2)
    await schedule_update_service.init()
    result_schedules = schedule_update_service.get_schedules()

    schedule_update_fetcher.init.assert_called_once_with()
    schedule_update_fetcher.fetch_updates.assert_called_once_with()
    assert result_schedules is schedules
    subscriber_1.assert_called_once_with(updates)
    subscriber_2.assert_called_once_with(updates)


@mark.asyncio
async def test_start_checking_for_updates() -> None:
    schedules = [schedule]
    updates = [(schedule, [Group('ИС-20-Д')])]
    fetch_result = schedules, updates
    schedule_update_fetcher.fetch_updates = Mock(return_value=Task.from_value(fetch_result))
    future_1: Future[None] = Future()
    future_2: Future[None] = Future()
    fetch_interval.wait = Mock(side_effect=[future_1, future_2])
    subscriber_1 = Mock()
    subscriber_2 = Mock()

    schedule_update_service.subscribe_to_updates(subscriber_1)
    schedule_update_service.subscribe_to_updates(subscriber_2)
    task = create_task(schedule_update_service.start_checking_for_updates())
    await sleep(0)
    fetch_interval.wait.assert_called_once_with()
    future_1.set_result(None)
    await sleep(0)
    result_schedules = schedule_update_service.get_schedules()

    assert result_schedules is schedules
    schedule_update_fetcher.fetch_updates.assert_called_once_with()
    subscriber_1.assert_called_once_with(updates)
    subscriber_2.assert_called_once_with(updates)
    task.cancel()
