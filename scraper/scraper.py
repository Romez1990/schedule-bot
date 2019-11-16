from typing import Dict, List
from urllib.parse import quote
from bs4 import BeautifulSoup, Tag
import requests

from structures import (
    Schedule,
    Group,
    GroupSchedule,
    WeekDay,
    DaySchedule,
    Entry,
)


class Scraper:
    def fetch_schedule(self) -> Schedule:
        groups = self._fetch_groups()
        schedule = self._parse_groups(groups)
        return schedule

    def _fetch_groups(self) -> Dict[str, str]:
        soup = self._get_soup('http://edu.viti-mephi.ru/raspth')
        link_tags: List[Tag] = soup.select('.raspth_table .cell a')
        groups: Dict[str, str] = \
            {link.text: 'http://edu.viti-mephi.ru/raspth/list?name=' +
                        quote(link.text, encoding='cp1251')
             for link in link_tags}
        return groups

    def _parse_groups(self, groups: Dict[str, str]) -> Schedule:
        schedule = Schedule()
        for group_name, url in groups.items():
            soup = self._get_soup(url)
            day_tags: List[Tag] = \
                soup.select('.table_gp tr:not(:nth-child(1))')
            group_schedule = self._parse_days(day_tags)
            schedule[Group(group_name)] = group_schedule
        return schedule

    def _parse_days(self, day_tags: List[Tag]) -> GroupSchedule:
        group_schedule = GroupSchedule()
        for day_tag in day_tags:
            week_day: str = day_tag.select_one('td:nth-child(1)').text
            entry_tags: List[Tag] = day_tag.select('td:not(:nth-child(1))')
            day_schedule = self._parse_entries(entry_tags)
            group_schedule[WeekDay.from_text(week_day)] = day_schedule
        return group_schedule

    def _parse_entries(self, entry_tags: List[Tag]) -> DaySchedule:
        day_schedule = DaySchedule()
        for entry_tag in entry_tags:
            if not entry_tag.text.strip():
                if not day_schedule:
                    day_schedule.append(None)
                    continue
                else:
                    break

            entry = Entry()
            entry.subject = entry_tag.select_one('.predmet').text
            entry.kind = entry_tag.select_one('.type').text
            entry.teacher = entry_tag.select_one('.prepod').text
            entry.class_room = entry_tag.select_one('.kabinet').text
            day_schedule.append(entry)
        return day_schedule

    def _get_soup(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        return soup
