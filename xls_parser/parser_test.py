from pathlib import Path
from pytest import fixture
from .parser import Parser
from renderer import Renderer, Group, ScheduleKind


def test_render_our_groups(parser: Parser, part_of_file: Path,
                           renderer: Renderer) -> None:
    schedule = parser.parse(part_of_file)
    wanted_groups = [
        Group('4ПрИн-5.16'),
        Group('4ПрИн-5а.16'),
    ]
    wanted_schedule = schedule.filter(wanted_groups)
    renderer.render(wanted_schedule, ScheduleKind.week)
    renderer.render(wanted_schedule, ScheduleKind.week, 'dark')


def test_render_all_groups(parser: Parser, full_file: Path,
                           renderer: Renderer) -> None:
    schedule = parser.parse(full_file)
    for group in schedule.groups.keys():
        wanted_schedule = schedule.filter([group])
        renderer.render(wanted_schedule, ScheduleKind.week)
        renderer.render(wanted_schedule, ScheduleKind.week, 'dark')


@fixture
def full_file() -> Path:
    current_directory = Path(__file__).parent
    file_path = current_directory / 'test_files' / \
                'raspisanie_grupp_s_07_10_2019_0.xlsx'
    return file_path


@fixture
def part_of_file() -> Path:
    current_directory = Path(__file__).parent
    file_path = current_directory / 'test_files' / \
                'raspisanie_grupp_s_07_10_2019_0 (fourth year only).xlsx'
    return file_path


@fixture
def parser() -> Parser:
    return Parser()


@fixture
def renderer() -> Renderer:
    return Renderer()
