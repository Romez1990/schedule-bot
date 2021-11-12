from abc import ABCMeta
from pathlib import Path


class Paths(metaclass=ABCMeta):
    project_root: Path
    source_root: Path

    assets_root: Path
    message_texts_path: Path
