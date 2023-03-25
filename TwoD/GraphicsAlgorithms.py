from TwoD.Primitives import *
from typing import Optional
import math
from enum import Enum


def degrees_to_radians(angle: float) -> float:
    """Переводит градусы в радианы"""
    return angle * math.pi / 180


def radians_to_degrees(radians: float) -> float:
    """Переводит радианы в градусы"""
    return radians * 180 / math.pi


def rotate_point(point: PointVector, rotation_axis: PointVector, angle: float) -> PointVector:
    """Поворачивает точку point вокруг оси rotation_axis на угол angle градусов"""
    x = point.x
    y = point.y
    x0 = rotation_axis.x
    y0 = rotation_axis.y
    angle_rad = degrees_to_radians(angle)
    new_x = x0 + (x - x0) * math.cos(angle_rad) - (y - y0) * math.sin(angle_rad)
    new_y = y0 + (x - x0) * math.sin(angle_rad) + (y - y0) * math.cos(angle_rad)
    return PointVector(new_x, new_y)


def rotate_line(line: Line, rotation_axis: PointVector, angle: float) -> Line:
    """Поворачивает линию line вокруг оси rotation_axis на угол angle градусов"""
    rotated_p0 = rotate_point(line.p0, rotation_axis, angle)
    rotated_p1 = rotate_point(line.p1, rotation_axis, angle)
    return Line(rotated_p0, rotated_p1)


def cyrus_beck_algorithm(line: Line, borders: list[Border]) -> tuple[bool, Optional[Line]]:
    """
    Алгоритм Кируса-Бека
    Обрезает линию line, если она выходит за границы borders.
    Возвращает True, если линию надо отрисовывать и новые точки линии
    """
    p0 = line.p0
    p1 = line.p1
    t0 = 0  # Параметр начала вектора
    t1 = 1  # Параметр конца вектора
    line_vector = p1 - p0
    for border in borders:
        border_normal = border.get_normal()
        border_point = border.get_some_point()
        product = line_vector * border_normal

        if product == 0:  # Линия параллельна границе
            # Проверяем знак скалярного произведения
            q = border_normal * (p0 - border_point)
            if q >= 0:  # линия внутри границы
                continue
            else:  # < 0: линия за границей
                return False, None

        # Вычисляем параметр точки пересечения линии с границей
        t = -(border_normal * (p0 - border_point)) / (border_normal * line_vector)

        if product < 0:  # Линия идёт изнутри наружу
            if t < t0:  # Линия выходит за границу
                return False, None
            t1 = min(t1, t)
        if product > 0:  # Линия идёт снаружи внутрь
            if t > t1:  # Линия выходит за границу
                return False, None
            t0 = max(t0, t)
    new_p0 = p0 + line_vector * t0
    new_p1 = p0 + line_vector * t1
    new_line = Line(
        (new_p0.x, new_p0.y),
        (new_p1.x, new_p1.y),
    )
    return True, new_line


def point_inside_triangle(point: PointVector, a: PointVector, b: PointVector, c: PointVector):
    """Возвращает True, если точка point находится внутри треугольника abc"""

    ab = b - a
    bc = c - b
    ca = a - c

    ap = point - a
    bp = point - b
    cp = point - c

    cross1 = ab.cross_product(ap)
    cross2 = bc.cross_product(bp)
    cross3 = ca.cross_product(cp)

    return cross1 >= 0 and cross2 >= 0 and cross3 >= 0


class WindingOrder(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


def find_polygon_area_and_winding_order(points: list[PointVector]) -> tuple[float, WindingOrder]:
    """Находит площадь полигона и направление вращения его точек"""

    area = 0
    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]
        width = b.x - a.x
        height = (a.y + b.y) / 2
        area += width * height
    if area >= 0:
        return area, WindingOrder.COUNTERCLOCKWISE
    else:
        return -area, WindingOrder.CLOCKWISE


def get_item(arr: list, index: int):
    index = index % len(arr)
    return arr[index]


def polygon_to_triangles(points: list[PointVector]) -> list[Triangle]:
    """Находит треугольники полигона методом отсечения ушей"""

    triangles = []
    index_list = list(range(len(points)))

    while len(index_list) > 3:
        for i in range(len(index_list)):
            i_prev = get_item(index_list, i - 1)
            i_curr = get_item(index_list, i)
            i_next = get_item(index_list, i + 1)

            b = points[i_prev]
            a = points[i_curr]
            c = points[i_next]

            ab = b - a
            ac = c - a

            if ab.cross_product(ac) < 0:  # Угол острый, можно попробовать отсечь треугольник
                can_clip = True

                # Проверяем, входят ли другие точки в треугольник abc
                for index in index_list:
                    if index == i_prev or index == i_curr or index == i_next:
                        continue
                    point = points[index]
                    if point_inside_triangle(point, b, a, c):
                        can_clip = False
                        break

                # Обрезаем треугольник
                if can_clip:
                    triangles.append(Triangle(b, a, c))
                    del index_list[i]
                    break  # Начинаем сначала просмотр всех вершин

    triangles.append(Triangle(points[index_list[0]], points[index_list[1]], points[index_list[2]]))
    return triangles
