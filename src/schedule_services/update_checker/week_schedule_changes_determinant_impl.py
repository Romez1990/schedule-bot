from typing import (
    Sequence,
    Awaitable,
)

from schedule_services.schedule import (
    Schedule,
    Group,
)
from .week_schedule_changes_determinant import WeekScheduleChangesDeterminant


class WeekScheduleChangesDeterminantImpl(WeekScheduleChangesDeterminant):
    def get_changed_groups(self,
                           schedules: Sequence[Schedule]) -> Awaitable[Sequence[tuple[Schedule, Sequence[Group]]]]:
        ...
