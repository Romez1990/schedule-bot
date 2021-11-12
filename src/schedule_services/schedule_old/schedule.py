from __future__ import annotations
from typing import (
    Optional,
    Callable,
    Iterable,
    Iterator,
    Mapping,
)
from returns.maybe import Maybe

from src.immutable_collections import (
    List,
    Dict,
)
from .group import Group
from .group_schedule import GroupSchedule
from .day_of_week import DayOfWeek


class Schedule(Mapping[Group, GroupSchedule]):
    def __init__(self, group_schedules: Mapping[Group, GroupSchedule]) -> None:
        self.__group_schedules = Dict(group_schedules)

    def __iter__(self) -> Iterator[Group]:
        groups = list(self.__group_schedules)
        groups.sort()
        return iter(groups)

    def __getitem__(self, key: Group) -> GroupSchedule:
        return self.__group_schedules[key]

    def __len__(self) -> int:
        return len(self.__group_schedules)

    def map(self, func: Callable[[GroupSchedule], GroupSchedule]) -> Schedule:
        return Schedule({key: func(value) for key, value in self.__group_schedules.items()})

    def filter(self, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        group_schedules = List(groups) \
            .filter(self.__group_exists) \
            .map(self.__get_group_schedule) \
            .map(lambda t: (t[0], self.__try_select_day(t[1], day_of_week)))
        return Schedule({group: group_schedule for group, group_schedule in group_schedules})

    def __group_exists(self, group: Group) -> bool:
        return group in self.__group_schedules

    def __get_group_schedule(self, group: Group) -> tuple[Group, GroupSchedule]:
        return group, self.__group_schedules[group]

    def __try_select_day(self, group_schedule: GroupSchedule, day_of_week: Optional[DayOfWeek]) -> GroupSchedule:
        return Maybe.from_value(day_of_week) \
            .map(lambda day: GroupSchedule({day: group_schedule[day]})) \
            .value_or(group_schedule)
