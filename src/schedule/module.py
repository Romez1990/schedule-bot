from src.ioc_container import Module, Container
from .group_parser_interface import GroupParserInterface
from .group_parser import GroupParser
from .day_of_week_translator_interface import DayOfWeekTranslatorInterface
from .day_of_week_translator import DayOfWeekTranslator


class ScheduleModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(GroupParser).to(GroupParserInterface)
        container.bind(DayOfWeekTranslator).to(DayOfWeekTranslatorInterface)
