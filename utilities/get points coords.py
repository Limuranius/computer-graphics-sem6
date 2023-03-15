import pygame
pygame.init()
screen = pygame.display.set_mode([500, 500])


"""Утилита, с помощью которой можно прожать точки на экране и узнать их координаты"""


running = True
points = []
while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                screen.set_at((x, y), (255, 255, 255))
                print(x, y)
                points.append((x, y))
    pygame.display.flip()  # Обновление окна

print(points)
pygame.quit()
