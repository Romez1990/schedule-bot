from .database_error import DatabaseError


class TableAlreadyExistsError(DatabaseError):
    pass
