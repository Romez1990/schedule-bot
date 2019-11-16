class Entry:
    def __init__(self, subject: str = None, kind: str = None,
                 teacher: str = None, class_room: str = None):
        self.subject = '' if subject is None else subject
        self.kind = '' if kind is None else kind
        self.teacher = '' if teacher is None else teacher
        self.class_room = '' if class_room is None else class_room

    def __bool__(self) -> bool:
        return any([
            self.subject,
            self.kind,
            self.teacher,
            self.class_room,
        ])

    __nonzero__ = __bool__
