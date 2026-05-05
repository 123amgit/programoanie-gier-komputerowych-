import pyray as rl

from config import EXPLOSION_TIME, EXPLOSION_WIDTH


class Explosion:
    def __init__(self, x: float, y: float, target_radius: float):
        self.x = x
        self.y = y
        self.target_radius = target_radius
        self.time = 0.0
        self.duration = EXPLOSION_TIME
        self.alive = True

    def update(self, dt: float) -> None:
        self.time += dt
        if self.time >= self.duration:
            self.alive = False

    def draw(self) -> None:
        progress = min(self.time / self.duration, 1.0)
        radius = self.target_radius * progress
        alpha = int(255 * (1.0 - progress))
        color = rl.Color(255, 180, 40, alpha)
        rl.draw_circle_lines(int(self.x), int(self.y), radius, color)

        if radius > 8:
            rl.draw_circle_lines(int(self.x), int(self.y), radius * 0.55, rl.Color(255, 80, 30, alpha))
