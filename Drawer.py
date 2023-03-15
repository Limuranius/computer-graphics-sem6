from pygame import Surface
from typing import Optional
import pygame
from Colors import Color

WIDTH = 1000
HEIGHT = 800

# Если True, то для отрисовки линии будет использоваться встроенный pygame.draw_line
# Иначе будет использоваться написанный здесь алгоритм Брезенхэма
USE_BUILTIN_DRAW_LINE = False

"""Рисует на экране и получает всякую информацию об экране"""

screen: Optional[Surface] = None  # Экран pygame'а, на котором будут рисоваться фигуры


def init():
    pygame.init()
    global screen
    screen = pygame.display.set_mode([WIDTH, HEIGHT])


def _bresenham_draw_line(p0: tuple[float, float], p1: tuple[float, float], color: Color = Color.WHITE):
    """Рисует линию, используя алгоритм Брезенхэма"""
    x1 = int(p0[0])
    y1 = int(p0[1])
    x2 = int(p1[0])
    y2 = int(p1[1])
    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dx_sign = -1 if (x2 - x1) < 0 else 1
    dy_sign = -1 if (y2 - y1) < 0 else 1
    if dx >= dy:  # Нужно двигаться по иксу
        # Переменная принятия решений, нужно ли изменять игрек
        # p < 0 - игрек остаётся таким же
        # p >= 0 - игрек нужно изменить
        p = 2 * dy - dx
        while x != x2:
            screen.set_at((x, y), color.value)
            x += dx_sign
            if p < 0:
                p += 2 * dy
            else:
                p += 2 * dy - 2 * dx
                y += dy_sign
    else:  # Нужно двигаться по игреку
        # Переменная принятия решений, нужно ли изменять икс
        # p < 0 - икс остаётся таким же
        # p >= 0 - икс нужно изменить
        p = 2 * dx - dy
        while y != y2:
            screen.set_at((x, y), color.value)
            y += dy_sign
            if p < 0:
                p += 2 * dx
            else:
                p += 2 * dx - 2 * dy
                x += dx_sign


def draw_line(p0: tuple[float, float], p1: tuple[float, float], color: Color = Color.WHITE):
    if USE_BUILTIN_DRAW_LINE:
        pygame.draw.line(screen, color.value, p0, p1)
    else:
        _bresenham_draw_line(p0, p1, color)


def fill_triangle(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float],
                  color: Color = Color.WHITE):
    pygame.draw.polygon(screen, color.value, [p0, p1, p2])


def fill_background(color: Color):
    screen.fill(color.value)


def update():
    pygame.display.flip()


def quit():
    pygame.quit()
