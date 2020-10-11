class GroupNameParsingError(Exception):
    def __init__(self, group_name: str) -> None:
        super().__init__(f'Cannot parse group name {group_name}')
        self.__group_name = group_name

    @property
    def group_name(self) -> str:
        return self.__group_name
