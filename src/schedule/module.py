from src.ioc_container import Module, ContainerBuilder
from .abstract_group_parser import AbstractGroupParser
from .group_parser import GroupParser
from .abstract_week_day_translator import AbstractWeekDayTranslator
from .week_day_translator import WeekDayTranslator


class ScheduleModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AbstractGroupParser).to(GroupParser)
        builder.bind(AbstractWeekDayTranslator).to(WeekDayTranslator)
