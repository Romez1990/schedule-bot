from __future__ import annotations
from typing import (
    Iterable,
    Callable,
)
from PIL import ImageFont

from infrastructure.ioc_container import service
from infrastructure.paths import Paths
from schedule_services.schedule import (
    Schedule,
    WeekSchedule,
    DayOfWeek,
    DayOfWeekTranslator,
    DaySchedule,
    Group,
    Entry,
)
from .schedule_renderer import ScheduleRenderer
from .image import Image
from .themes import (
    ThemeRepository,
    Theme,
    Color,
)
from .schedule_metrics import ScheduleMetrics


@service
class ScheduleRendererImpl(ScheduleRenderer):
    def __init__(self, themes: ThemeRepository, day_of_week_translator: DayOfWeekTranslator,
                 paths: Paths) -> None:
        self.__themes = themes
        self.__day_of_week_translator = day_of_week_translator
        self.__paths = paths

        quality = 3

        self._image: Image
        self._theme: Theme
        self._schedule_metrics: ScheduleMetrics

        self._scale = quality

        self._columns_width = {
            'class': self._scale * 130,
            'class_room': self._scale * 30,
        }
        self._columns_position = self._compute_offset(self._columns_width)

        self._rows_width = {
            'subject': self._scale * 14,
            'kind': self._scale * 9,
            'teacher': self._scale * 10,
        }
        self._rows_position: dict[str, int] = self._compute_offset(self._rows_width)

        self._cell_size = (
            sum(self._columns_width.values()),
            sum(self._rows_width.values()),
        )

        self._none_size = (
            round(self._cell_size[0] * 0.5),
            round(self._cell_size[1] * 0.03),
        )

        self._separator_width = round(self._cell_size[1] * 0.05)

        sidebar_columns = 2
        self._sidebar_stripe_width = self._cell_size[1]
        self._sidebar_width = sidebar_columns * self._sidebar_stripe_width + self._separator_width

        header_rows = 2
        header_row_height = self._cell_size[1]
        self._header_height = header_rows * header_row_height + self._separator_width

        self._fonts = {
            'Arial bold 16': self._load_font('Arial bold.ttf', 16),
            'Arial bold 14': self._load_font('Arial bold.ttf', 14),
            'Arial bold 8': self._load_font('Arial bold.ttf', 8),
            'Times New Roman bold 9': self._load_font('Times New Roman bold.ttf', 9),
            'Arial 6': self._load_font('Arial.ttf', 6),
            'Arial 7': self._load_font('Arial.ttf', 7),
            'Arial 8': self._load_font('Arial.ttf', 8),
        }

    def _compute_offset(self, values: dict[any, int]) -> dict[any, int]:
        offsets: dict[any, int] = {}
        current_offset = 0
        for key, value in values.items():
            offsets[key] = current_offset
            current_offset += value
        return offsets

    def _load_font(self, filename: str, font_size: int) -> ImageFont:
        font_path = self.__paths.fonts / filename
        return ImageFont.truetype(str(font_path), self._scale * font_size)

    def render(self, schedule: Schedule, theme_name: str) -> bytes:
        self._set_theme(theme_name)
        self._create_image(schedule)
        self._render_sidebar()
        self._render_header(schedule)
        self._render_schedule(schedule)
        return self._get_image_bytes()

    def _set_theme(self, theme_name: str) -> None:
        self._theme = self.__themes.get_by_name(theme_name).get_or_raise()

    def _get_nth_background_color(self, n: int) -> Color:
        background_color_index = n % len(self._theme.background_colors)
        return self._theme.background_colors[background_color_index]

    def _create_image(self, schedule: Schedule) -> None:
        self._schedule_metrics = ScheduleMetrics(schedule)
        image_size = (
            self._sidebar_width + self._schedule_metrics.groups_count * self._cell_size[0] +
            self._separator_width * (self._schedule_metrics.groups_count - 1),
            self._header_height + self._schedule_metrics.total_entries_count * self._cell_size[1] +
            self._separator_width * (self._schedule_metrics.days_count - 1),
        )
        self._image = Image(image_size, self._theme.text_color.to_tuple())

    def _get_position(self, group: int = None, day_of_week: DayOfWeek = None, entry: int = None) -> tuple[int, int]:
        x_position = y_position = 0
        if group is not None:
            x_position += self._sidebar_width + group * (self._cell_size[0] + self._separator_width)
        if day_of_week is not None:
            day_of_week_index = day_of_week.value - self._schedule_metrics.starts_from.value + 1
            day_index = day_of_week.value - self._schedule_metrics.starts_from.value
            day_offset = self._schedule_metrics.day_offsets[day_index]
            y_position += self._header_height + day_offset * self._cell_size[1] + \
                          day_of_week_index * self._separator_width
        if entry is not None:
            y_position += entry * self._cell_size[1]
        return x_position, y_position

    def _render_sidebar(self) -> None:
        self._render_sidebar_day_of_week(-1, (0, 0), 2)
        self._render_sidebar_entry_numbers(0, (0, 0), 1, '')
        self._render_sidebar_entry_numbers(1, (0, self._cell_size[1]), 1, '№')

        for day_index, day_of_week in enumerate(self._schedule_metrics.days_of_week):
            position = self._get_position(day_of_week=day_of_week)
            day_length = self._schedule_metrics.day_lengths[day_index]
            self._render_sidebar_day_of_week(day_index, position, day_length, day_of_week)
            self._render_sidebar_entry_numbers(self._schedule_metrics.day_offsets[day_index], position, day_length)

    def _render_sidebar_day_of_week(self, row_id: int, position: tuple[int, int], day_length: int,
                                    day_of_week: DayOfWeek = None) -> None:
        size = (self._sidebar_stripe_width,
                self._cell_size[1] * day_length)
        color = self._get_nth_background_color(row_id)
        self._image.rectangle(position, size, color.to_tuple())

        text = self.__day_of_week_translator.translate(day_of_week) if day_of_week is not None else ''
        if text:
            font = self._fonts['Arial bold 14']
            self._image.text_center_rotate(text, position, size, font)

    def _render_sidebar_entry_numbers(
            self, row_id: int, start_position: tuple[int, int],
            day_length: int, custom_text: str = None) -> None:
        font = self._fonts['Arial 8']
        for entry_number in range(day_length):
            position = (
                start_position[0] + self._sidebar_stripe_width,
                start_position[1] + entry_number * self._cell_size[1]
            )
            size = (self._sidebar_stripe_width, self._cell_size[1])
            color = self._get_nth_background_color(row_id + entry_number)
            self._image.rectangle(position, size, color.to_tuple())

            text = custom_text if custom_text is not None else str(entry_number + 1)
            self._image.text_center(text, position, size, font)

    def _render_stripe(self, row_id: int, position: tuple[int, int]) -> None:
        color = self._get_nth_background_color(row_id)
        self._image.rectangle(position, self._cell_size, color.to_tuple())

    def _render_header(self, groups: Iterable[Group]) -> None:
        for group_number, group in enumerate(groups):
            position = self._get_position(group_number)
            self._render_stripe(0, position)
            self._render_stripe(1, (position[0], position[1] + self._cell_size[1]))
            self._render_group(str(group), position)
            self._render_class_header(position)
            self._render_class_room_header(position)

    def _render_group(self, group: str, position: tuple[int, int]) -> None:
        font = self._fonts['Arial bold 16']
        self._image.text_center(group, position, self._cell_size, font)

    def _render_class_header(self, position: tuple[int, int]) -> None:
        text = 'Дисциплина, вид занятия, преподаватель'
        font = self._fonts['Arial bold 8']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._cell_size[1],
        )
        size = (self._columns_width['class'], self._cell_size[1])
        _, line_height = font.getsize(text)
        self._image.text_wrap_center(text, position, size, line_height, font)

    def _render_class_room_header(self, position: tuple[int, int]) -> None:
        text = 'Ауд.'
        font = self._fonts['Arial bold 8']
        position = (
            position[0] + self._columns_position['class_room'],
            position[1] + self._cell_size[1],
        )
        cell_size = (self._columns_width['class_room'], self._cell_size[1])
        self._image.text_center(text, position, cell_size, font)

    def _render_schedule(self, schedule: Schedule) -> None:
        for group_number, group in enumerate(schedule):
            for day_index, day_of_week in enumerate(self._schedule_metrics.days_of_week):
                for entry_number in range(self._schedule_metrics.day_lengths[day_index]):
                    position = self._get_position(group_number, day_of_week, entry_number)
                    row_number = self._schedule_metrics.day_offsets[day_index] + entry_number
                    self._render_stripe(row_number, position)
            week_schedule = schedule[group]
            self._render_week_schedule(week_schedule, group_number)

    def _render_week_schedule(self, week_schedule: WeekSchedule, group_number: int) -> None:
        for day_index, day_schedule in enumerate(week_schedule):
            day_of_week = DayOfWeek(week_schedule.starts_from.value + day_index)
            self._render_day_schedule(day_schedule, group_number, day_of_week)

    def _render_day_schedule(self, day_schedule: DaySchedule, group_number: int, day_of_week: DayOfWeek) -> None:
        for entry_number, maybe_entry in enumerate(day_schedule):
            position = self._get_position(group_number, day_of_week, entry_number)
            maybe_entry.match(self._draw_none(position), self._render_entry(position))

    def _draw_none(self, position: tuple[int, int]) -> Callable[[], None]:
        def draw_none() -> None:
            color = self._theme.text_color
            self._image.rectangle_center(position, self._cell_size, self._none_size, color.to_tuple())

        return draw_none

    def _render_entry(self, position: tuple[int, int]) -> Callable[[Entry], None]:
        def render_entry(entry: Entry) -> None:
            self._render_subject(entry.subject, position)
            self._render_kind(entry.kind, position)
            self._render_teacher(entry.teacher, position)
            self._render_class_room(entry.class_room, position)

        return render_entry

    def _render_subject(self, subject: str, position: tuple[int, int]) -> None:
        font = self._fonts['Times New Roman bold 9']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['subject'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['subject'])
        self._image.text_center(subject, position, cell_size, font)

    def _render_kind(self, kind: str, position: tuple[int, int]) -> None:
        font = self._fonts['Arial 6']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['kind'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['kind'])
        self._image.text_center(kind, position, cell_size, font)

    def _render_teacher(self, teacher: str, position: tuple[int, int]) -> None:
        font = self._fonts['Arial 7']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['teacher'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['teacher'])
        self._image.text_center(teacher, position, cell_size, font)

    def _render_class_room(self, class_room: str,
                           position: tuple[int, int]) -> None:
        font = self._fonts['Arial 8']
        position = (
            position[0] + self._columns_position['class_room'],
            position[1],
        )
        cell_size = (self._columns_width['class_room'], self._cell_size[1])
        _, line_height = font.getsize(class_room)
        self._image.text_wrap_center(class_room, position, cell_size, line_height, font)

    def _get_image_bytes(self) -> bytes:
        return self._image.get_bytes()
