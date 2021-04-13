class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def __eq__(self, other):
        return self.__x == other.x and self.__y == other.__y

    def __str__(self):
        return "x: {0}, y: {1}".format(self.__x, self.__y)

    def __hash__(self):
        return hash((self.__x, self.__y))


