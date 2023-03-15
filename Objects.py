from Primitives import *
import Drawer
from BaseObjects import BaseObject, BaseBorder
from math import sqrt, cos, sin, pi
from GraphicsAlgorithms import degrees_to_radians, radians_to_degrees
import GraphicsAlgorithms
import time


class LineObject(BaseObject):
    color = Color.WHITE

    def __init__(self, p0: tuple[float, float], p1: tuple[float, float],
                 rotation_axis: tuple[float, float] = (0, 0), border: BaseBorder | None = None):
        super().__init__(PointVector(*rotation_axis), border)
        self.edges = [Line(p0, p1)]


class Polygon(BaseObject):
    color = Color.WHITE

    def __init__(self, points: list[tuple[float, float] | PolarPoint],
                 rotation_axis: tuple[float, float] = (0, 0), border: BaseBorder | None = None):
        super().__init__(PointVector(*rotation_axis), border)
        if len(points) <= 2:
            raise Exception("Нельзя сделать многоугольник из стольких точек")

        # Переводим все полярные точки в декартовые
        for i, point in enumerate(points):
            if isinstance(point, PolarPoint):
                points[i] = point.to_cartesian().to_tuple()

        self.edges = []
        start = points[0]
        for i in range(1, len(points)):
            end = points[i]
            edge = Line(start, end)
            self.edges.append(edge)
            start = end
        self.edges.append(Line(points[-1], points[0]))

    def draw_triangles(self):
        points = [self.edges[0].p0]
        for edge in self.edges[:-1]:
            points.append(edge.p1)
        triangles = GraphicsAlgorithms.polygon_to_triangles(points)
        for triangle in triangles:
            triangle.draw()


class PythagorasTree(BaseObject):
    color = Color.WHITE

    def __init__(self, corner: tuple[float, float], edge_len: float,
                 alpha: float, phi: float, n: int, rotation_axis: tuple[float, float] = (0, 0),
                 border: BaseBorder | None = None):
        super().__init__(PointVector(*rotation_axis), border)
        self.edges = []
        self.recursive_create_edges(corner, edge_len, degrees_to_radians(alpha), degrees_to_radians(phi), n)

    def recursive_create_edges(self, corner: tuple[float, float], edge_len: float,
                               alpha: float, phi: float, n: int):
        if n == 0:
            return
        x, y = corner
        x1 = x + edge_len * cos(alpha)
        y1 = y + edge_len * sin(alpha)
        x2 = x + edge_len * sqrt(2) * cos(alpha - pi / 4)
        y2 = y + edge_len * sqrt(2) * sin(alpha - pi / 4)
        x3 = x + edge_len * cos(alpha - pi / 2)
        y3 = y + edge_len * sin(alpha - pi / 2)
        x4 = x3 + edge_len * cos(phi) * cos(alpha - phi)
        y4 = y3 + edge_len * cos(phi) * sin(alpha - phi)
        self.edges += [
            Line((x, y), (x1, y1)),
            Line((x, y), (x3, y3)),
            Line((x1, y1), (x2, y2)),
            Line((x2, y2), (x3, y3)),
            Line((x2, y2), (x4, y4)),
            Line((x3, y3), (x4, y4)),
        ]
        left_len = sqrt((x2 - x4) ** 2 + (y2 - y4) ** 2)
        right_len = sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
        left_alpha = alpha - phi + pi / 2
        right_alpha = alpha - phi
        # self.draw()
        # Drawer.update()
        # time.sleep(3)
        self.recursive_create_edges((x3, y3), right_len, right_alpha, phi, n - 1)
        self.recursive_create_edges((x4, y4), left_len, left_alpha, phi, n - 1)
