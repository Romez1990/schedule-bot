from __future__ import annotations
from pathlib import Path
from io import BytesIO
from typing import Tuple, Dict, Iterable, Any
from PIL import ImageFont
from returns.maybe import Nothing

from src.schedule import (
    Schedule,
    Group,
    GroupSchedule,
    DayOfWeek,
    DayOfWeekTranslatorInterface,
    DaySchedule,
)
from .schedule_renderer_interface import ScheduleRendererInterface
from .image import Image
from .themes import themes, Theme
from .schedule_metrics import ScheduleMetrics


class ScheduleRenderer(ScheduleRendererInterface):
    def __init__(self, day_of_week_translator: DayOfWeekTranslatorInterface) -> None:
        self.__day_of_week_translator = day_of_week_translator

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
        self._rows_position: Dict[str, int] = \
            self._compute_offset(self._rows_width)

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
        self._sidebar_width = sidebar_columns * self._sidebar_stripe_width + \
                              self._separator_width

        header_rows = 2
        header_row_height = self._cell_size[1]
        self._header_height = header_rows * header_row_height + \
                              self._separator_width

        self._fonts = {
            'Arial bold 16': self._load_font('fonts/Arial bold.ttf', 16),
            'Arial bold 14': self._load_font('fonts/Arial bold.ttf', 14),
            'Arial bold 8': self._load_font('fonts/Arial bold.ttf', 8),
            'Times New Roman bold 9':
                self._load_font('fonts/Times New Roman bold.ttf', 9),
            'Arial 6': self._load_font('fonts/Arial.ttf', 6),
            'Arial 7': self._load_font('fonts/Arial.ttf', 7),
            'Arial 8': self._load_font('fonts/Arial.ttf', 8),
        }

    def _compute_offset(self, values: Dict[Any, int]) -> Dict[Any, int]:
        offsets: Dict[Any, int] = {}
        current_offset = 0
        for key, value in values.items():
            offsets[key] = current_offset
            current_offset += value
        return offsets

    def _load_font(self, path: str, font_size: int) -> ImageFont:
        return ImageFont.truetype(
            str(Path(__file__).parent / Path(path)),
            self._scale * font_size)

    def render(self, schedule: Schedule, theme_name: str) -> BytesIO:
        self._set_theme(theme_name)
        self._create_image(schedule)
        self._render_sidebar()
        self._render_header(schedule)
        self._render_schedule(schedule)
        return self._save_image()

    def _set_theme(self, theme_name: str) -> None:
        try:
            self._theme = themes[theme_name]
        except KeyError:
            raise ValueError(f'Theme {theme_name} does not exists')

    def _create_image(self, schedule: Schedule) -> None:
        self._schedule_metrics = ScheduleMetrics(schedule)
        image_size = (
            self._sidebar_width +
            self._schedule_metrics.groups * self._cell_size[0] +
            self._separator_width *
            (self._schedule_metrics.groups - 1),
            self._header_height +
            self._schedule_metrics.entries * self._cell_size[1] +
            self._separator_width *
            (len(self._schedule_metrics.days_of_week) - 1),
        )
        self._image = Image(image_size, self._theme.text_color)

    def _get_position(self, group: int = None, day_of_week: DayOfWeek = None,
                      entry: int = None) -> Tuple[int, int]:
        x_position = y_position = 0
        if group is not None:
            x_position += self._sidebar_width + group * \
                          (self._cell_size[0] + self._separator_width)
        if day_of_week is not None:
            y_position += self._header_height + \
                          self._schedule_metrics.days_offsets[day_of_week] * \
                          self._cell_size[1] + \
                          self._schedule_metrics.days_of_week.index(day_of_week) * \
                          self._separator_width
        if entry is not None:
            y_position += entry * self._cell_size[1]
        return x_position, y_position

    def _render_sidebar(self) -> None:
        self._render_sidebar_day_of_week(-1, (0, 0), 2)
        self._render_sidebar_entry_numbers(0, (0, 0), 1, '')
        self._render_sidebar_entry_numbers(1, (0, self._cell_size[1]), 1, '№')

        for day_number, day_of_week in enumerate(self._schedule_metrics.days_of_week):
            position = self._get_position(day_of_week=day_of_week)
            self._render_sidebar_day_of_week(
                day_number, position, self._schedule_metrics[day_of_week],
                day_of_week)
            self._render_sidebar_entry_numbers(
                self._schedule_metrics.days_offsets[day_of_week], position,
                self._schedule_metrics[day_of_week])

    def _render_sidebar_day_of_week(
            self, row_id: int, position: Tuple[int, int], day_length: int,
            day_of_week: DayOfWeek = None) -> None:
        size = (self._sidebar_stripe_width,
                self._cell_size[1] * day_length)
        stripe_number = row_id % len(self._theme.stripes)
        color = self._theme.stripes[stripe_number]
        self._image.rectangle(position, size, color)

        text = self.__day_of_week_translator.translate(day_of_week) if day_of_week is not None else ''
        if text:
            font = self._fonts['Arial bold 14']
            self._image.text_center_rotate(text, position, size, font)

    def _render_sidebar_entry_numbers(
            self, row_id: int, start_position: Tuple[int, int],
            day_length: int, custom_text: str = None) -> None:
        font = self._fonts['Arial 8']
        for entry_number in range(day_length):
            position = (
                start_position[0] + self._sidebar_stripe_width,
                start_position[1] + entry_number * self._cell_size[1]
            )
            size = (self._sidebar_stripe_width,
                    self._cell_size[1])
            stripe_number = (row_id + entry_number) % len(self._theme.stripes)
            color = self._theme.stripes[stripe_number]
            self._image.rectangle(position, size, color)

            if custom_text is not None:
                text = custom_text
            else:
                text = str(entry_number + 1)
            self._image.text_center(text, position, size, font)

    def _render_stripe(self, row_id: int, position: Tuple[int, int]) -> None:
        stripe_number = row_id % len(self._theme.stripes)
        color = self._theme.stripes[stripe_number]
        self._image.rectangle(position, self._cell_size, color)

    def _render_header(self, groups: Iterable[Group]) -> None:
        for group_number, group in enumerate(groups):
            position = self._get_position(group_number)
            self._render_stripe(0, position)
            self._render_stripe(1,
                                (position[0], position[1] + self._cell_size[1]))
            self._render_group(str(group), position)
            self._render_class_header(position)
            self._render_class_room_header(position)

    def _render_group(self, group: str, position: Tuple[int, int]) -> None:
        font = self._fonts['Arial bold 16']
        self._image.text_center(group, position, self._cell_size, font)

    def _render_class_header(self, position: Tuple[int, int]) -> None:
        text = 'Дисциплина, вид занятия, преподаватель'
        font = self._fonts['Arial bold 8']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._cell_size[1],
        )
        size = (self._columns_width['class'],
                self._cell_size[1])
        _, line_height = font.getsize(text)
        self._image.text_wrap_center(text, position, size, line_height, font)

    def _render_class_room_header(self, position: Tuple[int, int]) -> None:
        text = 'Ауд.'
        font = self._fonts['Arial bold 8']
        position = (
            position[0] + self._columns_position['class_room'],
            position[1] + self._cell_size[1],
        )
        cell_size = (self._columns_width['class_room'],
                     self._cell_size[1])
        self._image.text_center(text, position, cell_size, font)

    def _render_schedule(self, schedule: Schedule) -> None:
        for group_number, group in enumerate(schedule):
            for day_of_week in self._schedule_metrics.days_of_week:
                for entry_number in range(self._schedule_metrics[day_of_week]):
                    position = self._get_position(group_number, day_of_week,
                                                  entry_number)
                    row_number = self._schedule_metrics.days_offsets[
                                     day_of_week] + entry_number
                    self._render_stripe(row_number, position)
            group_schedule = schedule[group]
            self._render_group_schedule(group_schedule, group_number)

    def _render_group_schedule(self, group_schedule: GroupSchedule,
                               group_number: int) -> None:
        for day_of_week in group_schedule:
            day_schedule = group_schedule[day_of_week]
            self._render_day_schedule(day_schedule, group_number, day_of_week)

    def _render_day_schedule(self, day_schedule: DaySchedule,
                             group_number: int, day_of_week: DayOfWeek) -> None:
        for entry_number, maybe_entry in enumerate(day_schedule):
            position = self._get_position(group_number, day_of_week, entry_number)
            if maybe_entry == Nothing:
                self._draw_none(position)
            else:
                entry = maybe_entry.unwrap()
                self._render_subject(entry.subject, position)
                self._render_kind(entry.kind, position)
                self._render_teacher(entry.teacher, position)
                self._render_class_room(entry.class_room, position)

    def _draw_none(self, position: Tuple[int, int]) -> None:
        color = self._theme.text_color
        self._image.rectangle_center(position, self._cell_size,
                                     self._none_size, color)

    def _render_subject(self, subject: str, position: Tuple[int, int]) -> None:
        font = self._fonts['Times New Roman bold 9']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['subject'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['subject'])
        self._image.text_center(subject, position, cell_size, font)

    def _render_kind(self, kind: str, position: Tuple[int, int]) -> None:
        font = self._fonts['Arial 6']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['kind'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['kind'])
        self._image.text_center(kind, position, cell_size, font)

    def _render_teacher(self, teacher: str, position: Tuple[int, int]) -> None:
        font = self._fonts['Arial 7']
        position = (
            position[0] + self._columns_position['class'],
            position[1] + self._rows_position['teacher'],
        )
        cell_size = (self._columns_width['class'],
                     self._rows_width['teacher'])
        self._image.text_center(teacher, position, cell_size, font)

    def _render_class_room(self, class_room: str,
                           position: Tuple[int, int]) -> None:
        font = self._fonts['Arial 8']
        position = (
            position[0] + self._columns_position['class_room'],
            position[1],
        )
        cell_size = (self._columns_width['class_room'],
                     self._cell_size[1])
        _, line_height = font.getsize(class_room)
        self._image.text_wrap_center(class_room, position, cell_size,
                                     line_height, font)

    def _save_image(self) -> BytesIO:
        return self._image.save()
