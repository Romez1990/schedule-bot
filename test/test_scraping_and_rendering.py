from pytest import fixture

from scraper import Scraper
from renderer import Renderer
from structures import ScheduleKind, Group


def test_render_our_groups(scraper: Scraper, renderer: Renderer) -> None:
    schedule = scraper.fetch_schedule()
    schedule = schedule.filter([
        Group('4ПрИн-5.16'),
        Group('4ПрИн-5а.16'),
    ])
    renderer.render(schedule, ScheduleKind.week, 'light')
    renderer.render(schedule, ScheduleKind.week, 'dark')


@fixture
def scraper() -> Scraper:
    return Scraper()


@fixture
def renderer() -> Renderer:
    return Renderer()
