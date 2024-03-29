from itertools import dropwhile
from typing import (
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    GroupSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from net.http_client import HttpClient
from data.html_parser import (
    HtmlParser,
    Document,
    TagElement,
    TextElement,
)
from data.fp.task_either import TaskEither
from data.fp.maybe import Maybe, Some, Nothing
from data.vector import List
from .group_schedule_scraper import GroupScheduleScraper


@service
class GroupScheduleScraperImpl(GroupScheduleScraper):
    def __init__(self, http_client: HttpClient, html_parser: HtmlParser) -> None:
        self.__http_client = http_client
        self.__html_parser = html_parser

    def scrap_group_schedule(self, link: str) -> TaskEither[Exception, GroupSchedule]:
        return self.__http_client.get_text(link) \
            .map(self.__html_parser.parse) \
            .map(self.__scrap_from_document)

    def __scrap_from_document(self, document: Document) -> GroupSchedule:
        day_elements = document.select_all('tr')[2:]
        day_schedules = day_elements.map(self.__get_day_schedule)
        starts_from, truncated_days = self.__truncate_days(DayOfWeek.monday, day_schedules)
        return GroupSchedule(starts_from, truncated_days)

    def __truncate_days(self, starts_from: DayOfWeek, days: List[DaySchedule]) -> tuple[DayOfWeek, List[DaySchedule]]:
        truncated_from_start = list(dropwhile(DaySchedule.is_empty, days))
        new_starts_from = DayOfWeek(starts_from.value + len(days) - len(truncated_from_start))
        truncated_days = list(dropwhile(DaySchedule.is_empty, reversed(days)))
        return new_starts_from, List(reversed(truncated_days))

    def __get_day_schedule(self, day_element: TagElement) -> DaySchedule:
        entry_tags = day_element.select_all('td p')[1:]
        entries = entry_tags.map(self.__get_entry)
        truncated_entries = self.__truncate_entries(entries)
        if len(truncated_entries) == 0:
            return DaySchedule.empty
        return DaySchedule(truncated_entries)

    def __truncate_entries(self, entries: List[Maybe[Entry]]) -> list[Maybe[Entry]]:
        truncated_entries = dropwhile(lambda entry: entry == Nothing, reversed(entries))
        return list(reversed(list(truncated_entries)))

    def __get_entry(self, entry_tag: TagElement) -> Maybe[Entry]:
        entry_tag_children = entry_tag.children
        if self.__is_entry_empty(entry_tag):
            return Nothing
        kind_and_subject, _, teacher_and_class_room, *_ = entry_tag_children
        if not isinstance(kind_and_subject, TextElement) or not isinstance(teacher_and_class_room, TextElement):
            raise ValueError('unexpected children type')
        kind, subject = self.__split_kind_and_subject(kind_and_subject.text)
        teacher, class_room = self.__split_teacher_and_class_room(teacher_and_class_room.text)
        return Some(Entry(subject, kind, teacher, class_room))

    def __is_entry_empty(self, entry_tag: TagElement) -> bool:
        entry_tag_children = entry_tag.children
        if len(entry_tag_children) == 0:
            return True
        first_entry_tag_child = entry_tag_children[0]
        return isinstance(first_entry_tag_child, TextElement) and first_entry_tag_child.text.strip() == '_'

    __kind_and_subject_splitters = [
        '.',
        'КР/КП',
    ]

    def __split_kind_and_subject(self, kind_and_subject: str) -> tuple[str, str]:
        return List(self.__kind_and_subject_splitters) \
            .find_first_map(self.__split_string(kind_and_subject)) \
            .get_or(('', kind_and_subject))

    def __split_string(self, string: str) -> Callable[[str], Maybe[tuple[str, str]]]:
        def split_string(splitter: str) -> Maybe[tuple[str, str]]:
            try:
                split_index = string.index(splitter) + len(splitter)
            except ValueError:
                return Nothing
            first_part = string[:split_index].strip()
            second_part = string[split_index:].strip()
            return Some((first_part, second_part))

        return split_string

    def __split_teacher_and_class_room(self, teacher_and_class_room: str) -> tuple[str, str]:
        split_str = 'а.'
        split_index = teacher_and_class_room.index(split_str)
        teacher = teacher_and_class_room[:split_index].strip()
        class_room = teacher_and_class_room[split_index + len(split_str):].strip()
        return teacher, class_room
