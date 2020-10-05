class Entry:
    def __init__(self, subject: str, kind: str, teacher: str, class_room: str) -> None:
        self.__subject = subject
        self.__kind = kind
        self.__teacher = teacher
        self.__class_room = class_room

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def teacher(self) -> str:
        return self.__teacher

    @property
    def class_room(self) -> str:
        return self.__class_room
