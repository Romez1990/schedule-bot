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
from data.vector import List
from schedule_services.schedule.group import Group
from .schedule_links_scraper import ScheduleLinksScraper
from .schedule_links_elements import ScheduleLinksElements


@service
class ScheduleLinksScraperImpl(ScheduleLinksScraper):
    def __init__(self, http_client: HttpClient, html_parser: HtmlParser) -> None:
        self.__http_client = http_client
        self.__html_parser = html_parser
        self.__week_start_and_end_regex = compile_regex(r'(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})')

    def scrap_schedule_links(self) -> TaskEither[Exception, Sequence[ScheduleLinks]]:
        return self.__http_client.html('https://viti-mephi.ru/raspisanie') \
            .map(self.__html_parser.parse) \
            .map(self.__scrap_from_document)

    def __scrap_from_document(self, document: Document) -> Sequence[ScheduleLinks]:
        return document.select_all('.node-raspisanie') \
            .map(self.__get_schedule_elements) \
            .filter(self.__is_week_element_valid) \
            .map(self.__get_schedule_links_)

    def __get_schedule_elements(self, week_element: TagElement) -> ScheduleLinksElements:
        links_element = week_element.select('.rasp_div')
        title = week_element.select('h2').text
        return ScheduleLinksElements(links_element, title)

    def __is_week_element_valid(self, schedule_links_elements: ScheduleLinksElements) -> bool:
        if schedule_links_elements.links_element is None:
            return False
        if 'заочного' in schedule_links_elements.title:
            return False
        return True

    def __get_schedule_links_(self, schedule_links_elements: ScheduleLinksElements) -> ScheduleLinks:
        start, end = self.__get_week_start_and_end(schedule_links_elements.title)
        groups = self.__parse_links_element(schedule_links_elements.links_element)
        return ScheduleLinks(start, end, groups)

    def __parse_links_element(self, links_element: TagElement) -> Mapping[Group, str]:
        return {self.__get_group(link_element): self.__get_link(links_element)
                for link_element in links_element.select_all('a')}

    def __get_group(self, link_element: TagElement) -> Group:
        return Group(link_element.text)

    def __get_link(self, link_element: TagElement) -> str:
        maybe_link = link_element.get_attribute('href')
        return maybe_link.get_or_raise()

    def __get_week_start_and_end(self, title: str) -> tuple[date, date]:
        start, end = List(self.__week_start_and_end_regex.findall(title)) \
            .map(self.__get_date_from_match)
        return start, end

    def __get_date_from_match(self, match: tuple[str, str, str]) -> date:
        day, month, year = map(int, match)
        return date(year, month, day)
