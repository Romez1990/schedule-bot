from typing import (
    Optional,
)


class ServiceBindParameters:
    def __init__(self, service: type, to_self: Optional[bool]) -> None:
        self.service = service
        self.to_self = to_self if to_self is not None else False
