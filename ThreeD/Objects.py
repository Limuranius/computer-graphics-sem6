import numpy as np
from abc import ABC
from Colors import ColorType, Color
import ThreeD.Matrices as Matrices
import Drawer


def parse_obj_file(file_path: str) -> tuple[list[tuple[float, float, float, float]], list[tuple[int, int]]]:
    vertices = []
    edges = []
    with open(file_path, "r") as f:
        verts_str, edges_str = f.read().split("#")
        for vert in verts_str.strip().split("\n"):
            x, y, z = [float(num) for num in vert.split()]
            vertices.append((x, y, z, 1))
        for edge in edges_str.strip().split("\n"):
            start, end = [int(num) for num in edge.split()]
            edges.append((start, end))
    return vertices, edges


class Camera:
    x: float
    y: float
    z: float
    fov: float

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.fov = 90


class FrameObject(ABC):
    """Трёхмерный объект в виде рамки, т.е. без заливки полигонов"""
    vertices: np.ndarray  # Трёхмерные однородные координаты точек, хранящиеся в матрице 4 * n, n - кол-во точек
    edges: list[tuple[int, int]]  # Рёбра. Содержит индексы на точки, соединённые между собой ребром

    x: float
    y: float
    z: float
    size: float
    x_angle: float
    y_angle: float
    z_angle: float
    color: ColorType

    def __init__(self, file_path: str, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.size = 50
        self.x_angle = 0
        self.y_angle = 0
        self.z_angle = 0
        self.color = Color.WHITE
        vertices, edges = parse_obj_file(file_path)
        self.vertices = np.array(vertices).transpose()
        self.edges = edges

    def get_transformation_matrix(self, camera: Camera) -> np.ndarray:
        rotate_x = Matrices.x_rotation_matrix(self.x_angle)
        rotate_y = Matrices.y_rotation_matrix(self.y_angle)
        rotate_z = Matrices.z_rotation_matrix(self.z_angle)
        stretch = Matrices.stretch_matrix(self.size)
        translate = Matrices.translate_matrix(self.x, self.y, self.z)
        # projection = Matrices.no_perspective_projection_matrix()
        # projection = Matrices.simple_perspective_projection_matrix(100)
        projection = Matrices.perspective_projection_matrix(
            fov=camera.fov,
            scr_width=Drawer.screen_width(),
            scr_height=Drawer.screen_height()
        )
        stretch_projection = Matrices.stretch_matrix_2d(Drawer.screen_width(), Drawer.screen_height())
        translate_to_centrer_screen = Matrices.translate_matrix_2d(
            Drawer.screen_width() // 2,
            Drawer.screen_height() // 2
        )
        """
        Порядок:
            1. Увеличить
            2. Повернуть по оси X, затем по оси Y, затем по оси Z
            3. Передвинуть по координатам x, y, z объекта
            4. Проецировать на экран (перевести трёхмерные координаты в двухмерные). При этом координаты нормализуются
            5. Увеличить координаты до размеров экрана
            6. Сдвинуть всё на середину экрана (чтобы центр камеры был не в левом верхнем углу а по середине)
        """
        result = translate_to_centrer_screen @ stretch_projection @ projection @ translate @ rotate_z @ rotate_y @ rotate_x @ stretch
        return result

    def draw(self, camera: Camera):
        transformation_matrix = self.get_transformation_matrix(camera)
        new_vertices = transformation_matrix @ self.vertices
        for start, end in self.edges:
            x0, y0, w0 = new_vertices[:, start]
            x1, y1, w1 = new_vertices[:, end]
            Drawer.draw_line((x0 / w0, y0 / w0), (x1 / w1, y1 / w1), self.color)
