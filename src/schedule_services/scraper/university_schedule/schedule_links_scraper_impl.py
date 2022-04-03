from re import compile as compile_regex
from datetime import date
from typing import (
    Sequence,
    Mapping,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import ScheduleLinks
from net.http_client import HttpClient
from data.html_parser import (
    HtmlParser,
    Document,
    TagElement,
)
from data.fp.task_either import TaskEither
from schedule_services.schedule.group import Group
from .schedule_links_scraper import ScheduleLinksScraper
from .schedule_links_elements import ScheduleLinksElements


@service
class ScheduleLinksScraperImpl(ScheduleLinksScraper):
    def __init__(self, http_client: HttpClient, html_parser: HtmlParser) -> None:
        self.__http_client = http_client
        self.__html_parser = html_parser
        self.__starts_at_regex = compile_regex(r'(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})')

    def scrap_schedules_links(self) -> TaskEither[Exception, Sequence[ScheduleLinks]]:
        return self.__http_client.get_text('https://viti-mephi.ru/raspisanie') \
            .map(self.__html_parser.parse) \
            .map(self.__scrap_from_document)

    def __scrap_from_document(self, document: Document) -> Sequence[ScheduleLinks]:
        return document.select_all('.node-raspisanie') \
            .map(self.__get_schedule_elements) \
            .filter(self.__is_week_element_valid) \
            .map(self.__get_schedule_links)

    def __get_schedule_elements(self, week_element: TagElement) -> ScheduleLinksElements:
        links_element = week_element.select('.rasp_div')
        title = week_element.select('h2').get_or_raise().text
        return ScheduleLinksElements(links_element, title)

    def __is_week_element_valid(self, schedule_links_elements: ScheduleLinksElements) -> bool:
        if schedule_links_elements.links_element.is_nothing:
            return False

        skip_phrases = [
            'заочного',
            'сессия',
        ]
        for skip_phrase in skip_phrases:
            if skip_phrase in schedule_links_elements.title:
                return False

        return True

    def __get_schedule_links(self, schedule_links_elements: ScheduleLinksElements) -> ScheduleLinks:
        start = self.__get_starts_at(schedule_links_elements.title)
        groups = self.__parse_links_element(schedule_links_elements.links_element.get_or_raise())
        return ScheduleLinks(start, groups)

    def __parse_links_element(self, links_element: TagElement) -> Mapping[Group, str]:
        return {self.__get_group(link_element): self.__get_link(link_element)
                for link_element in links_element.select_all('a')}

    def __get_group(self, link_element: TagElement) -> Group:
        return Group(link_element.text)

    def __get_link(self, link_element: TagElement) -> str:
        maybe_link = link_element.get_attribute('href')
        return maybe_link.get_or_raise()

    def __get_starts_at(self, title: str) -> date:
        match = self.__starts_at_regex.search(title)
        if match is None:
            raise RuntimeError
        day, month, year = map(int, match.groups())
        return date(year, month, day)
