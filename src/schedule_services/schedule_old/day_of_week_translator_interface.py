from .day_of_week import DayOfWeek


class DayOfWeekTranslatorInterface:
    def translate(self, day_of_week: DayOfWeek) -> str:
        raise NotImplementedError
