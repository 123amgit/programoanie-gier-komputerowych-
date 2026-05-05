"""
bullet.py
=========

Klasa pocisku.

Pocisk jest dynamicznym obiektem:
- pojawia się po naciśnięciu SPACE,
- leci w kierunku statku,
- ma ograniczony czas życia TTL,
- po trafieniu lub po czasie znika z listy.

W Lab 08 zostawiamy mechanikę pocisków z Lab 07,
bo potrzebujemy jej do punktacji i podziału asteroid.
"""

import math
import pyray as rl

from config import BULLET_RADIUS, BULLET_SPEED, BULLET_TTL
from utils import ghost_positions, wrap_position


class Bullet:
    """
    Pojedynczy pocisk wystrzelony przez statek.
    """

    def __init__(self, x: float, y: float, angle_deg: float):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL
        self.alive = True

        # Kierunek pocisku musi być taki sam jak kierunek przodu statku.
        # Nie dodajemy tutaj +90 ani -90, bo statek już trzyma poprawny kąt.
        angle_rad = math.radians(angle_deg)
        self.vx = math.cos(angle_rad) * BULLET_SPEED
        self.vy = math.sin(angle_rad) * BULLET_SPEED

    def update(self, dt: float) -> None:
        """
        Aktualizuje pozycję pocisku i jego czas życia.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x, self.y = wrap_position(self.x, self.y)

        self.ttl -= dt

        if self.ttl <= 0:
            self.alive = False

    def draw(self) -> None:
        """
        Rysuje pocisk jako małe żółte koło.
        """
        for draw_x, draw_y in ghost_positions(self.x, self.y, self.radius):
            rl.draw_circle(int(draw_x), int(draw_y), self.radius, rl.YELLOW)
