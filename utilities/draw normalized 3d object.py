import pygame
from TwoD.Primitives import PointVector
import os

pygame.init()
screen = pygame.display.set_mode([500, 500])

"""
Утилита, с помощью которой можно нарисовать многоугольник и сохранить его в файл
Координаты сохраняются в нормализованном виде
Направление вращение переводится на по часовой стрелке
"""

POLYGONS_DIR = "../ThreeD/Objects"


def draw_polygon(polygon: list[tuple[float, float]]) -> None:
    for i in range(1, len(polygon)):
        start = polygon[i - 1]
        end = polygon[i]
        pygame.draw.line(screen, (255, 255, 255), start, end)
    if len(polygon) >= 3:
        pygame.draw.line(screen, (0, 0, 255), polygon[-1], polygon[0])


def get_polygon_center(polygon: list[tuple[float, float]]) -> tuple[float, float]:
    # Находим среднее от всех точек
    x_sum = 0
    y_sum = 0
    for x, y in polygon:
        x_sum += x
        y_sum += y
    return x_sum / len(polygon), y_sum / len(polygon)


def normalise_polygon(polygon: list[tuple[float, float]]) -> list[tuple[float, float]]:
    c_x, c_y = get_polygon_center(polygon)
    max_center_dx = 0
    max_center_dy = 0
    for x, y in polygon:
        max_center_dx = max(max_center_dx, abs(x - c_x))
        max_center_dy = max(max_center_dy, abs(y - c_y))
    normalised_points = []
    for x, y in polygon:
        norm_x = (x - c_x) / max_center_dx
        norm_y = (y - c_y) / max_center_dy
        normalised_points.append((norm_x, norm_y))
    return normalised_points


def polygon_to_3d_obj(points: list[tuple[float, float]]) -> tuple[list[tuple[float, float, float]], list[tuple[int, int]]]:
    front = [(x, y, 1) for x, y in points]
    back = [(x, y, -1) for x, y in points]
    n = len(front)
    edges = []
    for i in range(n):
        edges.append((i, i + n))
        edges.append((i, (i + 1) % n))
        edges.append((i + n, n + (i + 1) % n))
    return front + back, edges


def save_3d_obj_to_file(vertices: list[tuple[float, float, float]], edges: list[tuple[int, int]], file_name: str = None):
    if file_name is None:
        file_name = input("Название: ")
    file_path = os.path.join(POLYGONS_DIR, file_name + ".txt")
    with open(file_path, "w") as file:
        for x, y, z in vertices:
            file.write(f"{x} {y} {z}\n")
        file.write("#\n")
        for start, end in edges:
            file.write(f"{start} {end}\n")


def main():
    points = []
    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEBUTTONDOWN:
                    match event.button:
                        case 1:  # ЛКМ
                            x, y = pygame.mouse.get_pos()
                            points.append((x, y))
                        case 3:  # ПКМ
                            if points:
                                del points[-1]
        screen.fill((0, 0, 0))
        draw_polygon(points)
        pygame.display.flip()  # Обновление окна

    pygame.quit()
    points = normalise_polygon(points)
    points_3d, edges = polygon_to_3d_obj(points)
    save_3d_obj_to_file(points_3d, edges)



main()
