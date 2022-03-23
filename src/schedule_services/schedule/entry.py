class Entry:
    def __init__(self, subject: str, kind: str, teacher: str, class_room: str) -> None:
        self.subject = subject
        self.kind = kind
        self.teacher = teacher
        self.class_room = class_room

    def __repr__(self) -> str:
        fields = [
            self.subject,
            self.kind,
            self.teacher,
            self.class_room,
        ]
        fields_str = ', '.join(map(repr, fields))
        return f'{type(self).__name__}({fields_str})'
