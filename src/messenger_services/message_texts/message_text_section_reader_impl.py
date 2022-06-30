from pathlib import Path

from infrastructure.ioc_container import service
from data.vector import List
from infrastructure.paths import Paths
from .message_text_section_reader import MessageTextSectionReader
from .message_text_section import MessageTextSection


@service
class MessageTextSectionReaderImpl(MessageTextSectionReader):
    def __init__(self, paths: Paths) -> None:
        self.__paths = paths

    def get_sections(self) -> dict[str, MessageTextSection]:
        files = List(self.__paths.message_texts_path.iterdir()) \
            .map(self.__read_file)
        return {file.name: file for file in files}

    def __read_file(self, path: Path) -> MessageTextSection:
        if path.is_dir():
            raise Exception('there must be no directories inside message texts directory')

        content = path.read_text()
        return MessageTextSection(path, content)
