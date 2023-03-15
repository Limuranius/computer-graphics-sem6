from Primitives import Border
from BaseObjects import BaseBorder


class RectangleBorder(BaseBorder):
    def __init__(self, p0: tuple[float, float], p1: tuple[float, float]):
        # Определяем верхнюю левую точку и нижнюю правую
        x0 = min(p0[0], p1[0])
        x1 = max(p0[0], p1[0])
        y0 = min(p0[1], p1[1])
        y1 = max(p0[1], p1[1])
        self.edges = [
            Border((x0, y0), (x1, y0)),
            Border((x1, y0), (x1, y1)),
            Border((x1, y1), (x0, y1)),
            Border((x0, y1), (x0, y0)),
        ]


class PolygonBorder(BaseBorder):
    def __init__(self, points: list[tuple[float, float]]):
        if len(points) <= 2:
            raise Exception("Нельзя сделать многоугольник из стольких точек")
        self.edges = []
        start = points[0]
        for i in range(1, len(points)):
            end = points[i]
            edge = Border(start, end)
            self.edges.append(edge)
            start = end
        self.edges.append(Border(points[-1], points[0]))
