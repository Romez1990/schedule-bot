from dataclasses import dataclass, field

from .payload import Payload


@dataclass(frozen=True, eq=False)
class ButtonBase:
    text: str


@dataclass(frozen=True, eq=False)
class Button(ButtonBase):
    pass


@dataclass(frozen=True, eq=False)
class InlineButton(ButtonBase):
    payload: Payload = field(kw_only=True)
