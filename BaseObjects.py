from abc import ABC, abstractmethod
import Drawer
from Colors import Color
from Primitives import *
from GraphicsAlgorithms import *


class BaseDrawable(ABC):
    edges: list[Line]
    color: Color
    rotation_angle: float  # Угол поворота в градусах
    rotation_axis: PointVector  # Точка, вокруг которой крутится объект

    def draw(self):
        for edge in self.edges:
            p0, p1 = edge.to_tuples()
            Drawer.draw_line(
                p0,
                p1,
                self.color
            )


class BaseBorder(BaseDrawable, ABC):
    edges: list[Border]
    color = Color.RED

    def get_borders(self) -> list[Border]:
        return self.edges


class BaseObject(BaseDrawable, ABC):
    border: BaseBorder | None

    def __init__(self, rotation_axis: PointVector, border: BaseBorder | None = None):
        self.border = border
        self.rotation_axis = rotation_axis
        self.rotation_angle = 0

    def draw(self):
        for edge in self.edges:
            edge = rotate_line(edge, self.rotation_axis, self.rotation_angle)
            if self.border is not None:
                need_drawing, edge = cyrus_beck_algorithm(edge, self.border.get_borders())
            else:
                need_drawing = True
            if need_drawing:
                p0, p1 = edge.to_tuples()
                Drawer.draw_line(
                    p0,
                    p1,
                    self.color
                )
