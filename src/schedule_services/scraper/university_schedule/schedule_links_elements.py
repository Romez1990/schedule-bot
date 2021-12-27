from data.html_parser import TagElement


class ScheduleLinksElements:
    def __init__(self, links_element: TagElement, title: str) -> None:
        self.links_element = links_element
        self.title = title
