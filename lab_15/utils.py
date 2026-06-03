# utils.py
# Funkcje pomocnicze.

import math


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)


def circle_rect_collision(cx: float, cy: float, radius: float, rect) -> bool:
    """
    Sprawdza kolizję koła z prostokątem Raylib Rectangle.
    Używane dla kolizji ducha z półkami bibliotecznymi.
    """
    closest_x = clamp(cx, rect.x, rect.x + rect.width)
    closest_y = clamp(cy, rect.y, rect.y + rect.height)

    dx = cx - closest_x
    dy = cy - closest_y

    return dx * dx + dy * dy <= radius * radius
