class Block:
    def __init__(self, x_pos: int, y_pos, width: int, height: int) -> None:
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__width = width
        self.__height = height

    @property
    def x_pos(self) -> int:
        return self.__x_pos

    @property
    def y_pos(self) -> int:
        return self.__y_pos

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
