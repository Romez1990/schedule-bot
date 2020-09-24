from .week_day import WeekDay


class AbstractWeekDayTranslator:
    def translate(self, week_day: WeekDay) -> str:
        raise NotImplementedError
