from dataclasses import dataclass, field
from typing import (
    Sequence,
    MutableSequence,
)

from .button import (
    ButtonBase,
    Button,
    InlineButton,
)


@dataclass(frozen=True, eq=False, kw_only=True)
class KeyboardBase:
    buttons: MutableSequence[Sequence[ButtonBase]] = field(default_factory=list, init=False)

    def row(self, *buttons: ButtonBase) -> None:
        self.buttons.append(buttons)


@dataclass(frozen=True, eq=False, kw_only=True)
class Keyboard(KeyboardBase):
    resize: bool = False
    # one_time: bool = False

    def row(self, *buttons: Button) -> None:
        super().row(*buttons)


@dataclass(frozen=True, eq=False, kw_only=True)
class InlineKeyboard(KeyboardBase):
    def row(self, *buttons: InlineButton) -> None:
        super().row(*buttons)
