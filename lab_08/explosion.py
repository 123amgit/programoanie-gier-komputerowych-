"""
explosion.py
============

Animacja eksplozji.

Eksplozja jest osobnym obiektem z własnym czasem życia.
To pasuje do architektury gry:
- pociski mają alive,
- asteroidy mają alive,
- eksplozje też mają alive.

Dzięki temu wszystkie dynamiczne obiekty można czyścić jedną funkcją
keep_alive() z utils.py.
"""

import pyray as rl

from config import EXPLOSION_TIME


class Explosion:
    """
    Prosta animacja rozszerzającego się okręgu.
    """

    def __init__(self, x: float, y: float, target_radius: float):
        self.x = x
        self.y = y
        self.target_radius = target_radius
        self.time = 0.0
        self.duration = EXPLOSION_TIME
        self.alive = True

    def update(self, dt: float) -> None:
        """
        Przesuwa animację w czasie.
        """
        self.time += dt

        if self.time >= self.duration:
            self.alive = False

    def draw(self) -> None:
        """
        Rysuje dwa okręgi, które rosną i zanikają.
        """
        progress = min(self.time / self.duration, 1.0)
        radius = self.target_radius * progress
        alpha = int(255 * (1.0 - progress))

        outer_color = rl.Color(255, 180, 40, alpha)
        inner_color = rl.Color(255, 80, 30, alpha)

        rl.draw_circle_lines(int(self.x), int(self.y), radius, outer_color)

        if radius > 8:
            rl.draw_circle_lines(int(self.x), int(self.y), radius * 0.55, inner_color)
