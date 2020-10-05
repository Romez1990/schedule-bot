from src.ioc_container import Module, ContainerBuilder
from .abstract_group_parser import AbstractGroupParser
from .group_parser import GroupParser
from .abstract_day_of_week_translator import AbstractDayOfWeekTranslator
from .day_of_week_translator import DayOfWeekTranslator


class ScheduleModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractGroupParser).to(GroupParser)
        builder.bind(AbstractDayOfWeekTranslator).to(DayOfWeekTranslator)
