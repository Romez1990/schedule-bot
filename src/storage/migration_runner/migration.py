from typing import (
    Optional,
)


class Migration:
    create_table: str
    create_relationships: Optional[str]
