from data.fp.maybe import Maybe
from data.html_parser import TagElement


class ScheduleLinksElements:
    def __init__(self, links_element: Maybe[TagElement], title: str) -> None:
        self.links_element = links_element
        self.title = title
