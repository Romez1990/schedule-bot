from pytest import fixture

from schedule import DayOfWeek
from src.schedule.day_of_week_translator import DayOfWeekTranslator


@fixture(autouse=True)
def setup() -> None:
    global day_of_week_translator
    day_of_week_translator = DayOfWeekTranslator()


day_of_week_translator: DayOfWeekTranslator


def test_translate_returns_string() -> None:
    day_of_week = day_of_week_translator.translate(DayOfWeek.monday)

    assert day_of_week == 'Понедельник'
