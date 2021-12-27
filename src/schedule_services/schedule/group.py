class Group:
    def __init__(self, group_name: str) -> None:
        self.__group_name = group_name

    def __hash__(self) -> int:
        return hash(self.__group_name)

    def __str__(self) -> str:
        return self.__group_name
