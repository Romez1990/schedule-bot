from pfun import List

from src.schedule import (
    UniversityGroup,
    GroupParserInterface,
)
from src.schedule_services.parser import (
    PageParserInterface,
    Tag,
)
from .group_list_scraper_interface import GroupListScraperInterface


class GroupListScraper(GroupListScraperInterface):
    def __init__(self, page_parser: PageParserInterface, group_parser: GroupParserInterface) -> None:
        self.__page_parser = page_parser
        self.__group_parser = group_parser

    async def get_groups_and_links(self) -> dict[UniversityGroup, str]:
        document = await self.__page_parser.parse('http://www.viti-mephi.ru/raspisanie')
        groups_and_links = List(document.select_all('.table_raspisanie a')) \
            .map(self.__get_group_and_link) \
            .filter(self.__is_university_group_acceptable)
        return {group: link for group, link in groups_and_links}

    def __get_group_and_link(self, group_tag: Tag) -> tuple[UniversityGroup, str]:
        group_name = group_tag.text.strip()
        group = self.__group_parser.parse_university_group(group_name).unwrap()
        group_link = group_tag.get_attribute('href')
        return group, group_link

    def __is_university_group_acceptable(self, t: tuple[UniversityGroup, str]) -> bool:
        group = t[0]
        return not str(group.form).startswith('З')
