from returns.maybe import Maybe, Some, Nothing

from src.schedule import (
    GroupSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from src.utilities import ListHelper
from src.schedule_services.parser import (
    PageParserInterface,
    Tag,
)
from .group_schedule_scraper_interface import GroupScheduleScraperInterface


class GroupScheduleScraper(GroupScheduleScraperInterface):
    def __init__(self, page_parser: PageParserInterface, list_helper: ListHelper) -> None:
        self.__page_parser = page_parser
        self.__list_helper = list_helper

    async def get_group_schedule(self, group_link: str) -> GroupSchedule:
        document = await self.__page_parser.parse(group_link)
        days_of_week: List[DayOfWeek] = [day_of_week for day_of_week in DayOfWeek]
        table = document.select('table')
        day_tags = table.select_all('tr')[2:]
        day_schedules = [self.__get_day_schedule(day_tag) for day_tag in day_tags]
        group_schedule: Dict[DayOfWeek, DaySchedule] = \
            {day_of_week: day_schedule for day_of_week, day_schedule in zip(days_of_week, day_schedules)}
        return GroupSchedule(group_schedule)

    def __get_day_schedule(self, day_tag: Tag) -> DaySchedule:
        entry_tags = day_tag.select_all('td p')[1:]
        entries = [self.__get_entry(entry_tag) for entry_tag in entry_tags]
        return DaySchedule(entries)

    def __get_entry(self, entry_tag: Tag) -> Maybe[Entry]:
        entry_tag_children = entry_tag.children
        if self.__is_entry_empty(entry_tag):
            return Nothing
        kind_and_subject = entry_tag_children[0]
        teacher_and_class_room = entry_tag_children[2]
        if not isinstance(kind_and_subject, str) or not isinstance(teacher_and_class_room, str):
            raise ValueError('unexpected children type')
        kind, subject = self.__split_kind_and_subject(kind_and_subject)
        teacher, class_room = self.__split_teacher_and_class_room(teacher_and_class_room)
        return Some(Entry(subject, kind, teacher, class_room))

    def __is_entry_empty(self, entry_tag: Tag) -> bool:
        entry_tag_children = entry_tag.children
        if len(entry_tag_children) == 0:
            return True
        first_entry_tag_child = entry_tag_children[0]
        if isinstance(first_entry_tag_child, str) and first_entry_tag_child.strip() == '_':
            return True
        return False

    __kind_and_subject_splitters = [
        '.',
        'КР/КП',
    ]

    def __split_kind_and_subject(self, kind_and_subject: str) -> tuple[str, str]:
        result = self.__list_helper.find_first_map(
            self.__kind_and_subject_splitters, lambda splitter: self.__split_string(kind_and_subject, splitter))
        if result != Nothing:
            return result.unwrap()
        return '', kind_and_subject

    def __split_string(self, string: str, splitter: str) -> Maybe[tuple[str, str]]:
        try:
            split_index = string.index(splitter) + len(splitter)
        except ValueError:
            return Nothing
        first_part = string[:split_index].strip()
        second_part = string[split_index:].strip()
        return Some((first_part, second_part))

    def __split_teacher_and_class_room(self, teacher_and_class_room: str) -> tuple[str, str]:
        split_str = 'а.'
        split_index = teacher_and_class_room.index(split_str)
        teacher = teacher_and_class_room[:split_index].strip()
        class_room = teacher_and_class_room[split_index + len(split_str):].strip()
        return teacher, class_room
