import math
import pyray as rl

from config import SCREEN_W, SCREEN_H, BULLET_SPEED, BULLET_RADIUS, BULLET_TTL
from utils import ghost_positions


class Bullet:
    def __init__(self, x: float, y: float, angle_deg: float):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL
        self.alive = True

        angle_rad = math.radians(angle_deg)
        self.vx = math.cos(angle_rad) * BULLET_SPEED
        self.vy = math.sin(angle_rad) * BULLET_SPEED

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.wrap()

        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

    def wrap(self) -> None:
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self) -> None:
        for cx, cy in ghost_positions(self.x, self.y, self.radius):
            rl.draw_circle(int(cx), int(cy), self.radius, rl.YELLOW)
