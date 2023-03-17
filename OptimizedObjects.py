import numpy

from Colors import Color, ColorType
import numpy as np
import Drawer
from math import cos, sin, pi
import GraphicsAlgorithms
from Primitives import PointVector, Triangle


def np_array_to_points(points: np.ndarray) -> list[PointVector]:
    points_count = points.shape[1]
    result = []
    for col in range(points_count):
        x, y, w = points[:, col]
        result.append(PointVector(x, y))
    return result


def triangles_to_np_array(triangles: list[Triangle]) -> np.ndarray:
    points = []
    for triangle in triangles:
        points.append((triangle.p0.x, triangle.p0.y, 1))
        points.append((triangle.p1.x, triangle.p1.y, 1))
        points.append((triangle.p2.x, triangle.p2.y, 1))
    return np.array(points).transpose()


def rotation_matrix(angle: float) -> np.ndarray:
    """Возвращает матрицу поворота на angle градусов"""
    rad = GraphicsAlgorithms.degrees_to_radians(angle)
    mat = [
        [cos(rad), sin(rad), 0],
        [-sin(rad), cos(rad), 0],
        [0, 0, 1]
    ]
    return np.array(mat)


def stretch_matrix(factor: float) -> np.ndarray:
    """Возвращает матрицу масштабирования на коэффициент factor"""
    mat = [
        [factor, 0, 0],
        [0, factor, 0],
        [0, 0, 1]
    ]
    return np.array(mat)


def translate_matrix(dx: float, dy: float) -> numpy.ndarray:
    """Возвращает матрицу перемещения на dx и dy"""
    mat = [
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ]
    return np.array(mat)


def draw_polygon(points: numpy.ndarray, color: ColorType):
    """Рисует полигон по матрице координат"""
    points_count = points.shape[1]
    for i in range(1, points_count):
        x0, y0, w0 = points[:, i - 1]
        x1, y1, w1 = points[:, i]
        Drawer.draw_line((x0, y0), (x1, y1), color)
    x0, y0, w0 = points[:, -1]
    x1, y1, w1 = points[:, 0]
    Drawer.draw_line((x0, y0), (x1, y1), color)


class PolygonOptimized:
    """
    Оптимизированная версия полигона, использующая нормализованные координаты и матрицы для вычисления координат фигуры.
    Используются двухмерные однородные координаты.
    """
    points: np.ndarray  # Матрица 3 на n, где n - количество точек полигона
    color: ColorType
    x: float
    y: float
    axis_x: float = 0  # x оси вращения
    axis_y: float = 0  # y оси вращения
    angle: float = 0  # Угол в градусах
    size: float

    SHOW_TRIANGLES = True  # Показывать ли треугольники, из которых состоит полигон?
    triangles: np.ndarray  # Матрица 3 на 3*q, где q - кол-во треугольников
    triangles_color: list[ColorType]  # Цвет каждого треугольника

    def __init__(self, file_path: str, color: ColorType = Color.WHITE, x: float = 0, y: float = 0, size: float = 1):
        self.load_file(file_path)
        print(file_path, GraphicsAlgorithms.find_polygon_area_and_winding_order(np_array_to_points(self.points)))
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        if self.SHOW_TRIANGLES:
            self.calculate_triangles()

    def load_file(self, file_path: str) -> None:
        coords = []
        with open(file_path, "r") as file:
            for line in file.read().strip().split("\n"):
                x, y = [float(num) for num in line.split()]
                coords.append([x, y, 1])
        self.points = np.array(coords).transpose()

    def get_transformation_matrix(self) -> np.ndarray:
        rotate = rotation_matrix(self.angle)
        stretch = stretch_matrix(self.size)
        translate = translate_matrix(self.x, self.y)
        translate_to_axis = translate_matrix(self.axis_x, self.axis_y)
        """
        Порядок: увеличить, сдвинуть до оси поворота, повернуть, сдвинуть обратно, сдвинуть на координаты объекта
        """
        result = translate @ rotate @ stretch
        return result

    def draw(self):
        transformation_matrix = self.get_transformation_matrix()
        draw_polygon(transformation_matrix @ self.points, self.color)
        if self.SHOW_TRIANGLES:
            self.draw_triangles(transformation_matrix)

    def draw_triangles(self, transformation_matrix: np.ndarray):
        new_triangle_points = transformation_matrix @ self.triangles
        cols_count = new_triangle_points.shape[1]
        for col in range(0, cols_count, 3):
            x0, y0, w0 = new_triangle_points[:, col]
            x1, y1, w1 = new_triangle_points[:, col + 1]
            x2, y2, w2 = new_triangle_points[:, col + 2]
            color = self.triangles_color[col // 3]
            Drawer.fill_triangle((x0, y0), (x1, y1), (x2, y2), color)

    def calculate_triangles(self):
        """Находит треугольники этого полигона"""
        points = np_array_to_points(self.points)
        triangles = GraphicsAlgorithms.polygon_to_triangles(points)
        self.triangles_color = [Color.random() for _ in range(len(triangles))]
        self.triangles = triangles_to_np_array(triangles)
