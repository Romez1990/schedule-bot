from pathlib import Path

from infrastructure.ioc_container import service
from data.vector import List
from infrastructure.paths import message_texts_path
from .message_text_section_reader import MessageTextSectionReader
from .message_text_section import MessageTextSection


@service
class MessageTextSectionReaderImpl(MessageTextSectionReader):
    def get_sections(self) -> dict[str, MessageTextSection]:
        files = List(message_texts_path.iterdir()) \
            .map(self.__read_file)
        return {file.name: file for file in files}

    def __read_file(self, path: Path) -> MessageTextSection:
        if path.is_dir():
            raise Exception('there must be no directories inside message texts directory')

        with open(path, 'r') as file:
            content = file.read()
        return MessageTextSection(path, content)
