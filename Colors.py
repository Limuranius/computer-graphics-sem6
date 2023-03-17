from random import randint

ColorType = tuple[int, int, int]


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    @staticmethod
    def random() -> ColorType:
        return randint(0, 255), randint(0, 255), randint(0, 255)
