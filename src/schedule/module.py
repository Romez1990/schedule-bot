from src.ioc_container import Module, ContainerBuilder
from .group_parser_interface import GroupParserInterface
from .group_parser import GroupParser
from .day_of_week_translator_interface import DayOfWeekTranslatorInterface
from .day_of_week_translator import DayOfWeekTranslator


class ScheduleModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(GroupParser).to(GroupParserInterface)
        builder.bind(DayOfWeekTranslator).to(DayOfWeekTranslatorInterface)
