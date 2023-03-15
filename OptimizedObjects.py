import numpy

from Colors import Color
import numpy as np
import Drawer
from math import cos, sin, pi
from GraphicsAlgorithms import degrees_to_radians


def rotation_matrix(angle: float) -> np.ndarray:
    """Возвращает матрицу поворота на angle градусов"""
    rad = degrees_to_radians(angle)
    mat = [
        [cos(rad), sin(rad)],
        [-sin(rad), cos(rad)]
    ]
    return np.array(mat)


def stretch_matrix(factor: float) -> np.ndarray:
    """Возвращает матрицу масштабирования на коэффициент factor"""
    mat = [
        [factor, 0],
        [0, factor]
    ]
    return np.array(mat)


def draw_polygon(points: numpy.ndarray, color: Color):
    points_count = points.shape[1]
    for i in range(1, points_count):
        start = points[:, i - 1]
        end = points[:, i]
        Drawer.draw_line(start, end, color)
    Drawer.draw_line(points[:, -1], points[:, 0], color)


def move_matrix(matrix: numpy.ndarray, dx: float, dy: float) -> None:
    """Смещает матрицу с координатами на dx и dy. Изменяет подаваемую матрицу matrix"""
    matrix[0] += dx
    matrix[1] += dy


class PolygonOptimized:
    """
    Оптимизированная версия полигона, использующая нормализованные координаты и матрицы для вычисления координат фигуры
    """
    points: np.ndarray  # Матрица 2 на n, где n - количество точек полигона
    color: Color
    x: float
    y: float
    angle: float = 0  # Угол в градусах
    size: float

    def __init__(self, file_path: str, color: Color = Color.WHITE, x: float = 0, y: float = 0, size: float = 1):
        self.load_file(file_path)
        self.color = color
        self.x = x
        self.y = y
        self.size = size

    def load_file(self, file_path: str) -> None:
        coords = []
        with open(file_path, "r") as file:
            for line in file.read().strip().split("\n"):
                x, y = [float(num) for num in line.split()]
                coords.append([x, y])
        self.points = np.array(coords).transpose()

    def draw(self):
        rotated_coords = np.matmul(
            rotation_matrix(self.angle),
            self.points
        )
        stretched_coords = np.matmul(
            stretch_matrix(self.size),
            rotated_coords
        )
        move_matrix(stretched_coords, self.x, self.y)
        draw_polygon(stretched_coords, self.color)
