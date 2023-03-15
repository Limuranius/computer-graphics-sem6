from __future__ import annotations
import math
from dataclasses import dataclass
from abc import ABC, abstractmethod
import Drawer
from Colors import Color


@dataclass
class PointVector:  # Точка / Вектор
    x: float
    y: float

    def __add__(self, other) -> PointVector:  # v1 + v2
        return PointVector(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other) -> PointVector:  # v1 - v2
        return PointVector(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other):  # v1 * num / v1 * v2
        if isinstance(other, float | int):
            return PointVector(
                self.x * other,
                self.y * other
            )
        elif isinstance(other, PointVector):
            return self.x * other.x + self.y * other.y

    def __truediv__(self, number: float) -> PointVector:  # v1 / num
        return PointVector(
            self.x / number,
            self.y / number
        )

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def get_normal(self) -> PointVector:
        """Возвращает "правую" нормаль вектора"""
        return PointVector(
            -self.y,
            self.x
        )


@dataclass
class PolarPoint:
    radius: float
    angle: float  # Угол в градусах
    center: PointVector

    def __init__(self, radius: float, angle: float, center: tuple[float, float] = (0, 0)):
        self.radius = radius
        self.angle = angle
        self.center = PointVector(*center)

    def to_cartesian(self) -> PointVector:
        """Переводит точку из полярной в декартовую систему координат"""
        r = self.radius
        phi = self.angle * math.pi / 180
        x = self.center.x + r * math.cos(phi)
        y = self.center.y + r * math.sin(phi)
        return PointVector(x, y)


class BasePrimitive(ABC):
    color: Color

    @abstractmethod
    def draw(self):
        pass


class Line(BasePrimitive):
    p0: PointVector
    p1: PointVector

    def __init__(self, p0: tuple[float, float] | PointVector, p1: tuple[float, float] | PointVector,
                 color: Color = Color.WHITE):
        if isinstance(p0, tuple):
            self.p0 = PointVector(p0[0], p0[1])
        elif isinstance(p0, PointVector):
            self.p0 = p0
        else:
            raise Exception("Чзх???")

        if isinstance(p1, tuple):
            self.p1 = PointVector(p1[0], p1[1])
        elif isinstance(p1, PointVector):
            self.p1 = p1
        else:
            raise Exception("Чзх 2???")

        self.color = color

    def draw(self):
        Drawer.draw_line(
            (self.p0.x, self.p0.y),
            (self.p1.x, self.p1.y),
            self.color
        )

    def __repr__(self):
        return "<({}, {}), ({}, {})>".format(
            self.p0.x, self.p0.y,
            self.p1.x, self.p1.y,
        )

    def to_tuples(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """Переводит линию в две координаты в виде кортежей"""
        return (
            (self.p0.x, self.p0.y),
            (self.p1.x, self.p1.y),
        )


class Border(Line):
    def get_some_point(self) -> PointVector:
        """Возвращает точку, принадлежащую этой границе"""
        return (self.p0 + self.p1) / 2

    def get_normal(self) -> PointVector:
        """Возвращает "правую" нормаль границы"""
        line_vector = self.p1 - self.p0
        return line_vector.get_normal()


class Triangle(BasePrimitive):
    p0: PointVector
    p1: PointVector
    p2: PointVector

    def __init__(self, p0: tuple[float, float] | PointVector, p1: tuple[float, float] | PointVector,
                 p2: tuple[float, float] | PointVector, color: Color = Color.WHITE):
        if isinstance(p0, tuple):
            self.p0 = PointVector(*p0)
        elif isinstance(p0, PointVector):
            self.p0 = p0

        if isinstance(p1, tuple):
            self.p1 = PointVector(*p1)
        elif isinstance(p1, PointVector):
            self.p1 = p1

        if isinstance(p2, tuple):
            self.p2 = PointVector(*p2)
        elif isinstance(p2, PointVector):
            self.p2 = p2

        self.color = color

    def draw(self):
        Drawer.fill_triangle(
            self.p0.to_tuple(),
            self.p1.to_tuple(),
            self.p2.to_tuple(),
            self.color
        )
