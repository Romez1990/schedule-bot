from pathlib import Path

from infrastructure.ioc_container import service
from .paths import Paths

project_root = Path(__file__).parent.parent.parent.parent
source_root = project_root / 'src'


@service
class PathsImpl(Paths):
    def __init__(self) -> None:
        self.project_root = project_root
        self.source_root = source_root

        self.assets = self.project_root / 'assets'
        self.fonts = self.assets / 'fonts'
        self.message_texts_path = self.assets / 'message_texts'
