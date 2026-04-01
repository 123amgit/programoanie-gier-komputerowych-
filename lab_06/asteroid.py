import math
import random
import pyray as rl

from config import (
    SCREEN_W,
    SCREEN_H,
    ASTEROID_MIN_SPEED,
    ASTEROID_MAX_SPEED,
    ASTEROID_VERTICES,
)
from utils import rotate_point, ghost_positions


class Asteroid:
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

        speed_factor = max(0.2, 1.0 - (radius / 80.0))
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED) * speed_factor
        angle = random.uniform(0.0, math.tau)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.angle = random.uniform(0.0, math.tau)
        self.rot_speed = random.uniform(-1.2, 1.2)

        self.local_points = self._generate_shape(ASTEROID_VERTICES, radius)

    def _generate_shape(self, count: int, radius: float):
        points = []
        for i in range(count):
            a = (math.tau / count) * i
            r = random.uniform(radius * 0.75, radius * 1.2)
            px = math.cos(a) * r
            py = math.sin(a) * r
            points.append((px, py))
        return points

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.rot_speed * dt

    def wrap(self) -> None:
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self) -> None:
        for cx, cy in ghost_positions(self.x, self.y, self.radius):
            world_points = []
            for px, py in self.local_points:
                rx, ry = rotate_point(px, py, self.angle)
                world_points.append((cx + rx, cy + ry))

            for i in range(len(world_points)):
                x1, y1 = world_points[i]
                x2, y2 = world_points[(i + 1) % len(world_points)]
                rl.draw_line(int(x1), int(y1), int(x2), int(y2), rl.LIGHTGRAY)