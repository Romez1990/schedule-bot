from __future__ import annotations
from abc import ABCMeta
from dataclasses import dataclass
from typing import (
    ClassVar,
)


class Payload(metaclass=ABCMeta):
    type: ClassVar[str]
    none: ClassVar[Payload]


@dataclass
class NonePayload(Payload):
    type: ClassVar[str] = 'none'


Payload.none = NonePayload()
