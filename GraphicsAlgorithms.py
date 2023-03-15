from Primitives import *
from typing import Optional
import math


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


def polygon_to_triangles(points: list[PointVector]) -> list[Triangle]:
    # Добавляем в конец первый элемент и в начало последний чтобы не делать отдельных проверок на границы
    triangles = []
    old_points = [points[0]] + points + [points[-1]]
    while len(old_points) > 3:
        i = 1
        new_points = []  # Вершины урезанного полигона, после одной итерации
        while i <= len(old_points) - 2:
            p_prev = old_points[i-1]
            p_curr = old_points[i]
            p_next = old_points[i+1]

            # Проверяем, где находится точка
            vect = p_next - p_prev
            norm = vect.get_normal()
            mid_p_vect = p_curr - p_prev
            product = norm * mid_p_vect  # Скалярное произведения нормали и вектора до средней точки
            if product <= 0:  # Точка находится "слева"
                triangles.append(Triangle(p_prev, p_curr, p_next, Color.random()))
                if p_prev not in new_points:  # Нужно оптимизировать
                    new_points.append(p_prev)
                if p_next not in new_points:  # Нужно оптимизировать
                    new_points.append(p_next)
                i += 2
            else:  # Точка находится "справа"
                if p_curr not in new_points:  # Нужно оптимизировать
                    new_points.append(p_curr)
                i += 1
        old_points = new_points
    if len(old_points) == 3:
        triangles.append(Triangle(old_points[0], old_points[1], old_points[2], Color.random()))
    return triangles
