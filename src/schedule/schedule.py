from __future__ import annotations
from typing import (
    Optional,
    Tuple,
    Iterable,
    Iterator,
    Mapping,
)
from pyrsistent import PMap, pmap
from pfun import List
from returns.maybe import Maybe

from .group import Group
from .group_schedule import GroupSchedule
from .week_day import WeekDay


class Schedule(Mapping[Group, GroupSchedule]):
    def __init__(self, group_schedules: Mapping[Group, GroupSchedule]):
        self.__group_schedules = pmap(group_schedules)

    __group_schedules: PMap[Group, GroupSchedule]

    def __iter__(self) -> Iterator[Group]:
        return iter(sorted(self.__group_schedules))

    def __getitem__(self, key: Group) -> GroupSchedule:
        return self.__group_schedules[key]

    def __len__(self) -> int:
        return len(self.__group_schedules)

    def filter(self, groups: Iterable[Group], week_day: WeekDay = None) -> Schedule:
        group_schedules = List(groups) \
            .filter(self.__group_exists) \
            .map(self.__get_group_schedule) \
            .map(lambda t: (t[0], self.__try_select_day(t[1], week_day)))
        return Schedule({group: group_schedule for group, group_schedule in group_schedules})

    def __group_exists(self, group: Group) -> bool:
        return group in self.__group_schedules

    def __get_group_schedule(self, group: Group) -> Tuple[Group, GroupSchedule]:
        return group, self.__group_schedules[group]

    def __try_select_day(self, group_schedule: GroupSchedule, week_day: Optional[WeekDay]) -> GroupSchedule:
        return Maybe.from_value(week_day) \
            .map(lambda day: GroupSchedule({day: group_schedule[day]})) \
            .value_or(group_schedule)
