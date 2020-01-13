from pytest import fixture, raises

from renderer import Renderer
from structures import (
    Schedule,
    Group,
    GroupSchedule,
    WeekDay,
    DaySchedule,
    Entry,
)


def test_rendering_day(day_schedule: Schedule,
                       renderer: Renderer) -> None:
    renderer.render(day_schedule, 'dark')


def test_rendering_week(week_schedule: Schedule,
                        renderer: Renderer) -> None:
    renderer.render(week_schedule, 'dark')


def test_rendering_multi_group_day(
        multi_group_day_schedule: Schedule, renderer: Renderer) -> None:
    renderer.render(multi_group_day_schedule, 'dark')


def test_rendering_multiple_groups(multiple_groups_schedule: Schedule,
                                   renderer: Renderer) -> None:
    renderer.render(multiple_groups_schedule, 'dark')


def test_render_wrong_theme(day_schedule: Schedule, renderer: Renderer) -> None:
    with raises(ValueError):
        renderer.render(day_schedule, '123')


@fixture
def renderer() -> Renderer:
    return Renderer()


@fixture
def day_schedule() -> Schedule:
    return Schedule.day(Group('4ПрИн-5а.16'), WeekDay.monday, DaySchedule([
        None,
        Entry('ПМ03 МДК 03.012', '(лекция)', 'Конченко Е. А.', '2-404'),
        Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', '2-306к'),
        Entry('ПМ03 МДК 03.014', '(практ.)', 'Конченко Е. А.', '2-100к'),
    ]))


@fixture
def week_schedule(day_schedule: Schedule) -> Schedule:
    return Schedule.group(Group('4ПрИн-5а.16'), GroupSchedule({
        WeekDay.monday: day_schedule[Group('4ПрИн-5а.16')][WeekDay.monday],
        WeekDay.tuesday: DaySchedule([
            Entry('ПМ03 МДК 03.01', '(практ.)', 'Конченко Е. А.', '2-306к'),
            Entry('ПМ03 МДК 03.012', '(практ.)', 'Конченко Е. А.', '2-401'),
            Entry('БЖ', '(практ.)', 'Плотников Г.Н.', 'Л-207'),
        ]),
        WeekDay.wednesday: DaySchedule([
            None,
            None,
            None,
            Entry('ПМ03 МДК 03.012', '(практ.)', 'Конченко Е. А.', 'Л-207а'),
            Entry('ПМ04 МДК 04.012', '(практ.)', 'Янковская И. А.', 'Л-207а'),
            Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', '2-306к'),
        ]),
        WeekDay.thursday: DaySchedule([
            Entry('Менеджмент', '(лекция)', 'Митина Л. В.', '2-401'),
            Entry('БЖ', '(лекция)', 'Плотников Г.Н.', 'Л-207'),
            Entry('Ин. язык', '(практ.)', 'Рябчинская Т. В.', 'Л-214'),
            Entry('ПМ04 МДК 04.012', '(практ.)', 'Янковская И. А.', 'Л-207а'),
        ]),
        WeekDay.friday: DaySchedule([
            Entry('Физ-ра', '(практ.)', 'Коваленко С. П.', 'Спорт. зал3'),
            Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', 'Л-201'),
            Entry('ПМ04 МДК 04.012', '(лекция)', 'Янковская И. А.', 'Л-207'),
            Entry('Ком.сети', '(практ.)', 'Брежнев Е. А.', '2-306к'),
        ]),
    }))


@fixture
def multi_group_day_schedule(day_schedule: Schedule) -> Schedule:
    return Schedule({
        Group('4ПрИн-5а.16'): day_schedule[Group('4ПрИн-5а.16')],
        Group('4ПрИн-5.16'): GroupSchedule.day(WeekDay.monday, DaySchedule([
            None,
            Entry('ПМ03 МДК 03.012', '(лекция)', 'Конченко Е. А.', '2-404'),
            Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', '2-306к'),
            Entry('ПМ03 МДК 03.014', '(практ.)', 'Конченко Е. А.', '2-100к'),
        ])),
    })


@fixture
def multiple_groups_schedule(week_schedule: Schedule) -> Schedule:
    return Schedule({
        Group('4ПрИн-5а.16'): week_schedule[Group('4ПрИн-5а.16')],
        Group('4ПрИн-5.16'): GroupSchedule({
            WeekDay.monday: DaySchedule([
                Entry('ПМ03 МДК 03.012', '(лекция)', 'Конченко Е. А.', '2-404'),
                Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', '2-306к'),
                Entry('ПМ03 МДК 03.014', '(практ.)', 'Конченко Е. А.',
                      '2-100к'),
            ]),
            WeekDay.tuesday: DaySchedule([
                Entry('ПМ03 МДК 03.01', '(практ.)', 'Конченко Е. А.', '2-306к'),
                Entry('ПМ03 МДК 03.012', '(практ.)', 'Конченко Е. А.', '2-401'),
                Entry('БЖ', '(практ.)', 'Плотников Г.Н.', 'Л-207'),
            ]),
            WeekDay.wednesday: DaySchedule([
                None,
                None,
                None,
                Entry('ПМ03 МДК 03.012', '(практ.)', 'Конченко Е. А.',
                      'Л-207а'),
                Entry('ПМ04 МДК 04.012', '(практ.)', 'Янковская И. А.',
                      'Л-207а'),
                Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', '2-306к'),
            ]),
            WeekDay.thursday: DaySchedule([
                Entry('Менеджмент', '(лекция)', 'Митина Л. В.', '2-401'),
                Entry('БЖ', '(лекция)', 'Плотников Г.Н.', 'Л-207'),
                Entry('Ин. язык', '(практ.)', 'Рябчинская Т. В.', 'Л-214'),
                Entry('ПМ04 МДК 04.012', '(практ.)', 'Янковская И. А.',
                      'Л-207а'),
            ]),
            WeekDay.friday: DaySchedule([
                Entry('Физ-ра', '(практ.)', 'Коваленко С. П.', 'Спорт. зал3'),
                Entry('Ком.сети', '(лекция)', 'Брежнев Е. А.', 'Л-201'),
                Entry('ПМ04 МДК 04.012', '(лекция)', 'Янковская И. А.',
                      'Л-207'),
                Entry('Ком.сети', '(практ.)', 'Брежнев Е. А.', '2-306к'),
            ]),
        }),
    })
