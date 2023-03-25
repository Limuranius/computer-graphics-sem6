import math


def degrees_to_radians(angle: float) -> float:
    """Переводит градусы в радианы"""
    return angle * math.pi / 180


def radians_to_degrees(radians: float) -> float:
    """Переводит радианы в градусы"""
    return radians * 180 / math.pi
