import pygame

pygame.init()
screen = pygame.display.set_mode([500, 500])

"""Утилита, с помощью которой можно нарисовать многоугольник и получить его в нормализованном виде"""

running = True
points = []


def draw_polygon() -> None:
    for i in range(1, len(points)):
        start = points[i - 1]
        end = points[i]
        pygame.draw.line(screen, (255, 255, 255), start, end)
    if len(points) >= 3:
        pygame.draw.line(screen, (0, 0, 255), points[-1], points[0])


def normalise_polygon() -> list[tuple[float, float]]:
    c_x, c_y = get_polygon_center()
    max_center_dx = 0
    max_center_dy = 0
    for x, y in points:
        max_center_dx = max(max_center_dx, abs(x - c_x))
        max_center_dy = max(max_center_dy, abs(y - c_y))
    normalised_points = []
    for x, y in points:
        norm_x = (x - c_x) / max_center_dx
        norm_y = (y - c_y) / max_center_dy
        normalised_points.append((norm_x, norm_y))
    return normalised_points


def get_polygon_center() -> tuple[float, float]:
    # Находим среднее от всех точек
    x_sum = 0
    y_sum = 0
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
    return x_sum / len(points), y_sum / len(points)


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
                        print(get_polygon_center())
                    case 3:  # ПКМ
                        if points:
                            del points[-1]
    screen.fill((0, 0, 0))
    draw_polygon()
    pygame.display.flip()  # Обновление окна

print(points)
print(normalise_polygon())
pygame.quit()
