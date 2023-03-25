import ThreeD.GraphicsAlgorithms as GraphicsAlgorithms
import numpy as np
from math import cos, sin, tan


def x_rotation_matrix(angle: float) -> np.ndarray:
    """Возвращает матрицу поворота на angle градусов вокруг оси X"""
    rad = GraphicsAlgorithms.degrees_to_radians(angle)
    mat = [
        [1, 0, 0, 0],
        [0, cos(rad), -sin(rad), 0],
        [0, sin(rad), cos(rad), 0],
        [0, 0, 0, 1],
    ]
    return np.array(mat)


def y_rotation_matrix(angle: float) -> np.ndarray:
    """Возвращает матрицу поворота на angle градусов вокруг оси Y"""
    rad = GraphicsAlgorithms.degrees_to_radians(angle)
    mat = [
        [cos(rad), 0, sin(rad), 0],
        [0, 1, 0, 0],
        [-sin(rad), 0, cos(rad), 0],
        [0, 0, 0, 1],
    ]
    return np.array(mat)


def z_rotation_matrix(angle: float) -> np.ndarray:
    """Возвращает матрицу поворота на angle градусов вокруг оси Z"""
    rad = GraphicsAlgorithms.degrees_to_radians(angle)
    mat = [
        [cos(rad), -sin(rad), 0, 0],
        [sin(rad), cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    return np.array(mat)


def stretch_matrix(factor: float) -> np.ndarray:
    """Возвращает матрицу масштабирования на коэффициент factor"""
    mat = [
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ]
    return np.array(mat)


def stretch_matrix_2d(factor_x: float, factor_y: float) -> np.ndarray:
    """Возвращает матрицу масштабирования на коэффициент factor"""
    mat = [
        [factor_x, 0, 0],
        [0, factor_y, 0],
        [0, 0, 1]
    ]
    return np.array(mat)


def translate_matrix(dx: float, dy: float, dz: float) -> np.ndarray:
    """Возвращает матрицу перемещения на dx и dy"""
    mat = [
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1],
    ]
    return np.array(mat)


def translate_matrix_2d(dx: float, dy: float) -> np.ndarray:
    """Возвращает матрицу перемещения на dx и dy"""
    mat = [
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1],
    ]
    return np.array(mat)


def simple_perspective_projection_matrix(dist: float) -> np.ndarray:
    """Возвращает матрицу проекции трёхмерных координат на двухмерные с примитивной перспективой"""
    mat = [
        [dist, 0, 0, 0],
        [0, dist, 0, 0],
        [0, 0, 1, 0]
    ]
    return np.array(mat)


def no_perspective_projection_matrix() -> np.ndarray:
    """Возвращает матрицу проекции трёхмерных координат на двухмерные без перспективы"""
    mat = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ]
    return np.array(mat)


def perspective_projection_matrix(fov: float = 90, scr_width: float = 1, scr_height: float = 1, z_near: float = 0.1,
                                  z_far: float = 1000) -> np.ndarray:
    fov_rad = GraphicsAlgorithms.degrees_to_radians(fov)
    a = scr_height / scr_width
    f = 1 / tan(fov_rad / 2)
    q = z_far / (z_far - z_near)
    # mat = [
    #     [a * f, 0, 0, 0],
    #     [0, f, 0, 0],
    #     [0, 0, q, -z_near * q],
    #     [0, 0, 1, 0],
    # ]
    mat = [
        [a * f, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, 1, 0],
    ]
    return np.array(mat)


def test(point: tuple[float, float, float]):
    p = np.array(point + (1, )).transpose()
    m = perspective_projection_matrix(fov=90)
    new_p = m @ p
    return new_p / new_p[2]
    # return new_p


# print(test((100, 100, 100)))
