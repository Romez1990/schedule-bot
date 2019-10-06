from pathlib import Path
from .parser import Parser
from renderer import Renderer, Group, ScheduleKind


def test_parser() -> None:
    parser = Parser()
    current_directory = Path(__file__).parent
    file_path = current_directory / 'test_files' / \
                'raspisanie_grupp_s_07_10_2019_0 (fourth year only).xlsx'
    schedule = parser.parse(file_path)
    renderer = Renderer()
    wanted_groups = [
        Group('4ПрИн-5.16'),
        Group('4ПрИн-5а.16'),
    ]
    wanted_schedule = schedule.filter(wanted_groups)
    renderer.render(wanted_schedule, ScheduleKind.week)
    renderer.render(wanted_schedule, ScheduleKind.week, 'dark')
