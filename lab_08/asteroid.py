"""
asteroid.py
===========

Klasa asteroidy dla Lab 08.

Najważniejsza nowość:
- asteroida ma poziom level: 3, 2 albo 1,
- promień i prędkość wynikają z level,
- metoda split() zwraca dwie mniejsze asteroidy albo pustą listę.

To dokładnie odpowiada pierwszemu zadaniu z laboratorium:
podział asteroid powinien być odpowiedzialnością samej asteroidy,
bo to ona najlepiej wie, jaki ma poziom i co powinna zrobić po trafieniu.
"""

import math
import random
import pyray as rl

from config import (
    ASTEROID_RADIUS_BY_LEVEL,
    ASTEROID_SPEED_BY_LEVEL,
    ASTEROID_VERTICES,
)
from utils import ghost_positions, rotate_point, wrap_position


class Asteroid:
    """
    Asteroida poruszająca się po ekranie.

    level:
    - 3: duża asteroida,
    - 2: średnia asteroida,
    - 1: mała asteroida.

    Gdy duża lub średnia asteroida zostanie trafiona,
    split() tworzy dwie mniejsze asteroidy.
    """

    def __init__(self, x: float, y: float, level: int = 3):
        if level not in ASTEROID_RADIUS_BY_LEVEL:
            raise ValueError("Poziom asteroidy musi być równy 1, 2 albo 3.")

        self.x = x
        self.y = y
        self.level = level
        self.radius = ASTEROID_RADIUS_BY_LEVEL[level]
        self.alive = True

        self.vx, self.vy = self._random_velocity_for_level(level)

        self.angle = random.uniform(0.0, math.tau)
        self.rot_speed = random.uniform(-1.8, 1.8)

        self.local_points = self._generate_shape(ASTEROID_VERTICES, self.radius)

    def _random_velocity_for_level(self, level: int) -> tuple[float, float]:
        """
        Losuje prędkość asteroidy na podstawie poziomu.

        Mniejsze asteroidy mają większą prędkość.
        """
        min_speed, max_speed = ASTEROID_SPEED_BY_LEVEL[level]
        speed = random.uniform(min_speed, max_speed)
        angle = random.uniform(0.0, math.tau)

        velocity_x = math.cos(angle) * speed
        velocity_y = math.sin(angle) * speed

        return velocity_x, velocity_y

    def _generate_shape(self, count: int, radius: float) -> list[tuple[float, float]]:
        """
        Tworzy nieregularny wielokąt asteroidy.

        Punkty są rozłożone wokół okręgu, ale każdy ma lekko losowy promień.
        Dzięki temu asteroida nie wygląda jak idealne koło.
        """
        points = []

        for index in range(count):
            angle = (math.tau / count) * index
            local_radius = random.uniform(radius * 0.75, radius * 1.20)

            point_x = math.cos(angle) * local_radius
            point_y = math.sin(angle) * local_radius

            points.append((point_x, point_y))

        return points

    def split(self) -> list["Asteroid"]:
        """
        Dzieli asteroidę na dwie mniejsze.

        Zasada:
        - level 3 trafiony -> dwie asteroidy level 2,
        - level 2 trafiony -> dwie asteroidy level 1,
        - level 1 trafiony -> brak nowych asteroid.

        main.py nie musi znać szczegółów podziału.
        Po prostu wywołuje asteroid.split() i dodaje wynik do listy.
        """
        if self.level <= 1:
            return []

        next_level = self.level - 1
        children = []

        for _ in range(2):
            child = Asteroid(self.x, self.y, next_level)

            # Małe przesunięcie, żeby dzieci nie powstały idealnie w tym samym pikselu.
            child.x += random.uniform(-8.0, 8.0)
            child.y += random.uniform(-8.0, 8.0)

            children.append(child)

        return children

    def update(self, dt: float) -> None:
        """
        Aktualizuje pozycję i obrót asteroidy.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.rot_speed * dt

        self.x, self.y = wrap_position(self.x, self.y)

    def draw(self) -> None:
        """
        Rysuje asteroidę jako nieregularny obrys.

        Kolor zależy od poziomu, żeby było widać wielkość logiczną obiektu.
        """
        color = self._color_for_level()

        for draw_x, draw_y in ghost_positions(self.x, self.y, self.radius):
            world_points = []

            for local_x, local_y in self.local_points:
                rotated_x, rotated_y = rotate_point(local_x, local_y, self.angle)
                world_points.append((draw_x + rotated_x, draw_y + rotated_y))

            for index in range(len(world_points)):
                x1, y1 = world_points[index]
                x2, y2 = world_points[(index + 1) % len(world_points)]

                rl.draw_line(int(x1), int(y1), int(x2), int(y2), color)

    def _color_for_level(self):
        """
        Zwraca kolor asteroidy na podstawie poziomu.
        """
        if self.level == 3:
            return rl.LIGHTGRAY

        if self.level == 2:
            return rl.RAYWHITE

        return rl.YELLOW
