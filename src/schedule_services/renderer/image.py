from io import BytesIO
from PIL import Image as ImageBase, ImageDraw, ImageFont


class Image:
    def __init__(self, size: tuple[int, int], text_color: tuple[int, int, int]):
        self._image: ImageBase = ImageBase.new('RGB', size)
        self._draw: ImageDraw = ImageDraw.Draw(self._image)
        self._text_color = text_color

    def rectangle(self, start_position: tuple[int, int], size: tuple[int, int],
                  color: tuple[int, int, int]) -> None:
        position = [
            start_position,
            (start_position[0] + size[0],
             start_position[1] + size[1])
        ]
        self._draw.rectangle(position, color)

    def rectangle_center(
            self, cell_position: tuple[int, int], cell_size: tuple[int, int],
            size: tuple[int, int], color: tuple[int, int, int]) -> None:
        position = [
            (cell_position[0] + cell_size[0] / 2 - size[0] / 2,
             cell_position[1] + cell_size[1] / 2 - size[1] / 2),
            (cell_position[0] + cell_size[0] / 2 + size[0] / 2,
             cell_position[1] + cell_size[1] / 2 + size[1] / 2),
        ]
        self._draw.rectangle(position, color)

    def text_center(self, text: str, cell_position: tuple[int, int],
                    cell_size: tuple[int, int], font: ImageFont) -> None:
        text_size = font.getsize(text)
        text_image = ImageBase.new('RGBA', cell_size)
        text_draw = ImageDraw.Draw(text_image)
        text_position = (max(int((cell_size[0] - text_size[0]) / 2), 0),
                         max(int((cell_size[1] - text_size[1]) / 2), 0))
        text_draw.text(text_position, text, self._text_color, font)
        self._image.paste(text_image, cell_position, text_image)

    def text_center_rotate(self, text: str, cell_position: tuple[int, int],
                           cell_size: tuple[int, int], font: ImageFont) -> None:
        text_size = font.getsize(text)
        text_image = ImageBase.new('RGBA', (cell_size[1], cell_size[0]))
        text_draw = ImageDraw.Draw(text_image)
        text_position = (max(int((cell_size[1] - text_size[0]) / 2), 0),
                         max(int((cell_size[0] - text_size[1]) / 2), 0))
        text_draw.text(text_position, text, self._text_color, font)
        rotated_text_image = text_image.rotate(90, expand=1)
        self._image.paste(rotated_text_image, cell_position, rotated_text_image)

    def text_wrap_center(self, text: str, cell_position: tuple[int, int],
                         cell_size: tuple[int, int], line_height: int,
                         font: ImageFont) -> None:
        lines = self._wrap_text(text, font, cell_size[0])
        text_image = ImageBase.new('RGBA', cell_size)
        text_draw = ImageDraw.Draw(text_image)

        current_height = 0
        text_height = line_height * len(lines)
        if text_height < cell_size[1]:
            current_height = int((cell_size[1] - text_height) / 2)
        for i, line in enumerate(lines):
            text_size = font.getsize(line)
            position = (int((cell_size[0] - text_size[0]) / 2),
                        int(current_height + (line_height - text_size[1]) / 2))
            text_draw.text(position, line, self._text_color, font)
            current_height += line_height
        self._image.paste(text_image, cell_position, text_image)

    def _wrap_text(self, text: str, font: ImageFont, width: int) -> list[str]:
        words = text.split()
        lines = []
        line = ''
        for word in words:
            line_width = font.getsize(line + word)[0]
            if line_width > width:
                lines.append(line)
                line = word
                continue
            if line:
                line += ' '
            line += word
        if line:
            lines.append(line)
        return lines

    def get_bytes(self) -> bytes:
        bytes_io = BytesIO()
        self._image.save(bytes_io, 'JPEG')
        bytes_io.seek(0)
        return bytes_io.getvalue()
