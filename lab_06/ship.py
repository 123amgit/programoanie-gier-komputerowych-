import math
import pyray as rl

from config import (
    SCREEN_W,
    SCREEN_H,
    SHIP_THRUST,
    SHIP_ROT_SPEED,
    SHIP_FRICTION,
    SHIP_RADIUS,
    SHIP_MAX_SPEED,
)
from utils import rotate_point, clamp_speed, ghost_positions


class Ship:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.angle_deg = -90.0  # Up
        self.radius = SHIP_RADIUS

        # Ship shape in local coordinates
        self.local_points = [
            (0, -self.radius),
            (self.radius * 0.7, self.radius),
            (0, self.radius * 0.45),
            (-self.radius * 0.7, self.radius),
        ]

    def update(self, dt: float) -> None:
        if rl.is_key_down(rl.KEY_LEFT):
            self.angle_deg -= SHIP_ROT_SPEED * dt
        if rl.is_key_down(rl.KEY_RIGHT):
            self.angle_deg += SHIP_ROT_SPEED * dt

        angle_rad = math.radians(self.angle_deg)

        if rl.is_key_down(rl.KEY_UP):
            self.vx += math.cos(angle_rad) * SHIP_THRUST * dt
            self.vy += math.sin(angle_rad) * SHIP_THRUST * dt

        self.vx *= SHIP_FRICTION
        self.vy *= SHIP_FRICTION

        self.vx, self.vy = clamp_speed(self.vx, self.vy, SHIP_MAX_SPEED)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def wrap(self) -> None:
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self) -> None:
        angle_rad = math.radians(self.angle_deg)

        for cx, cy in ghost_positions(self.x, self.y, self.radius):
            world_points = []
            for px, py in self.local_points:
                rx, ry = rotate_point(px, py, angle_rad)
                world_points.append((cx + rx, cy + ry))

            for i in range(len(world_points)):
                x1, y1 = world_points[i]
                x2, y2 = world_points[(i + 1) % len(world_points)]
                rl.draw_line(int(x1), int(y1), int(x2), int(y2), rl.WHITE)

            # Small engine flame
            if rl.is_key_down(rl.KEY_UP):
                fx1, fy1 = rotate_point(-5, self.radius * 0.9, angle_rad)
                fx2, fy2 = rotate_point(0, self.radius * 1.5, angle_rad)
                fx3, fy3 = rotate_point(5, self.radius * 0.9, angle_rad)

                rl.draw_line(
                    int(cx + fx1), int(cy + fy1),
                    int(cx + fx2), int(cy + fy2),
                    rl.ORANGE
                )
                rl.draw_line(
                    int(cx + fx2), int(cy + fy2),
                    int(cx + fx3), int(cy + fy3),
                    rl.ORANGE
                )