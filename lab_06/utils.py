import math
from typing import List, Tuple

from config import SCREEN_W, SCREEN_H


def rotate_point(x: float, y: float, angle_rad: float) -> tuple[float, float]:

    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    rx = x * c - y * s
    ry = x * s + y * c
    return rx, ry


def clamp_speed(vx: float, vy: float, max_speed: float) -> tuple[float, float]:
    speed = math.hypot(vx, vy)
    if speed > max_speed and speed > 0:
        scale = max_speed / speed
        return vx * scale, vy * scale
    return vx, vy


def ghost_positions(x: float, y: float, size: float) -> List[Tuple[float, float]]:

    xs = [x]
    ys = [y]

    if x < size:
        xs.append(x + SCREEN_W)
    if x > SCREEN_W - size:
        xs.append(x - SCREEN_W)

    if y < size:
        ys.append(y + SCREEN_H)
    if y > SCREEN_H - size:
        ys.append(y - SCREEN_H)

    positions = []
    for px in xs:
        for py in ys:
            positions.append((px, py))
    return positions