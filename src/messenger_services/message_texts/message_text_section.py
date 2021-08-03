from pathlib import Path


class MessageTextSection:
    def __init__(self, file_path: Path, content: str) -> None:
        self.file_path = file_path
        self.content = content

    @property
    def name(self) -> str:
        return self.file_path.name
