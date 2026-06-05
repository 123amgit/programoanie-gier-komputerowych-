# particle.py
# Proste efekty wizualne używane przy zbieraniu i oddawaniu stron.

import random
import pyray as pr


class Particle:
    def __init__(self, x: float, y: float, color=None) -> None:
        self.x = x
        self.y = y
        self.vx = random.uniform(-70, 70)
        self.vy = random.uniform(-90, 40)
        self.life = random.uniform(0.35, 0.7)
        self.max_life = self.life
        self.radius = random.uniform(2, 5)

        if color is None:
            self.color = pr.Color(230, 220, 255, 255)
        else:
            self.color = color

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 90 * dt
        self.life -= dt

    def is_alive(self) -> bool:
        return self.life > 0

    def draw(self) -> None:
        alpha = int(255 * max(self.life / self.max_life, 0))
        color = pr.Color(self.color.r, self.color.g, self.color.b, alpha)
        pr.draw_circle(int(self.x), int(self.y), self.radius, color)


def create_sparkles(x: float, y: float, amount: int, color=None) -> list[Particle]:
    return [Particle(x, y, color) for _ in range(amount)]


def update_particles(particles: list[Particle], dt: float) -> None:
    for particle in particles:
        particle.update(dt)

    particles[:] = [particle for particle in particles if particle.is_alive()]


def draw_particles(particles: list[Particle]) -> None:
    for particle in particles:
        particle.draw()
