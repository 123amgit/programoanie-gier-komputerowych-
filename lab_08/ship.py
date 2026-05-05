"""
ship.py
=======

Klasa statku gracza.

W Lab 08 zostawiamy poprawioną wersję z Lab 07:
- kierunek ruchu,
- wizualny nos statku,
- kierunek pocisku,
wszystkie używają tego samego układu kątów.

To jest ważne, bo wcześniej przy złym kształcie lokalnym statek wyglądał,
jakby strzelał z boku. Tutaj przód statku jest lokalnie na osi X,
a ruch też używa cos(angle), sin(angle).
"""

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
from utils import clamp_speed, ghost_positions, rotate_point


class Ship:
    """
    Obiekt sterowany przez gracza.

    Statek ma pozycję, prędkość, kąt obrotu i promień kolizyjny.
    Kształt jest rysowany z kilku punktów lokalnych.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.vx = 0.0
        self.vy = 0.0

        # -90 stopni oznacza kierunek do góry ekranu.
        # W standardowej matematyce 0 stopni to prawo, więc -90 daje górę.
        self.angle_deg = -90.0

        self.radius = SHIP_RADIUS
        self.alive = True

        # Lokalny kształt statku.
        # Nos znajduje się w punkcie (radius, 0).
        # Dzięki temu wizualny przód zgadza się z wektorem ruchu.
        self.local_points = [
            (self.radius, 0),
            (-self.radius * 0.75, self.radius * 0.65),
            (-self.radius * 0.35, 0),
            (-self.radius * 0.75, -self.radius * 0.65),
        ]

    def get_angle_rad(self) -> float:
        """
        Zwraca kąt statku w radianach.

        Raylib i funkcje trygonometryczne pracują na radianach,
        dlatego przeliczamy stopnie tylko wtedy, gdy są potrzebne.
        """
        return math.radians(self.angle_deg)

    def get_forward_vector(self) -> tuple[float, float]:
        """
        Zwraca wektor kierunku przodu statku.

        Ten sam wektor jest używany do ruchu i do wyznaczania miejsca,
        z którego startuje pocisk.
        """
        angle_rad = self.get_angle_rad()
        return math.cos(angle_rad), math.sin(angle_rad)

    def get_nose_position(self, offset: float = 8.0) -> tuple[float, float]:
        """
        Zwraca pozycję czubka statku.

        offset przesuwa pocisk kilka pikseli przed statek,
        żeby nie wyglądało, że pocisk zaczyna się w środku modelu.
        """
        forward_x, forward_y = self.get_forward_vector()

        nose_x = self.x + forward_x * (self.radius + offset)
        nose_y = self.y + forward_y * (self.radius + offset)

        return nose_x, nose_y

    def reset(self) -> None:
        """
        Resetuje statek do pozycji startowej.

        W Lab 08 kolizja statku z asteroidą kończy grę,
        ale reset jest nadal przydatny przy rozpoczęciu nowej gry.
        """
        self.x = SCREEN_W / 2
        self.y = SCREEN_H / 2
        self.vx = 0.0
        self.vy = 0.0
        self.angle_deg = -90.0
        self.alive = True

    def update(self, dt: float) -> None:
        """
        Aktualizuje ruch statku na podstawie klawiatury.

        dt to czas jednej klatki.
        Dzięki temu statek działa podobnie przy różnych FPS.
        """
        if rl.is_key_down(rl.KEY_LEFT):
            self.angle_deg -= SHIP_ROT_SPEED * dt

        if rl.is_key_down(rl.KEY_RIGHT):
            self.angle_deg += SHIP_ROT_SPEED * dt

        if rl.is_key_down(rl.KEY_UP):
            forward_x, forward_y = self.get_forward_vector()
            self.vx += forward_x * SHIP_THRUST * dt
            self.vy += forward_y * SHIP_THRUST * dt

        # Tarcie daje efekt bezwładności.
        self.vx *= SHIP_FRICTION
        self.vy *= SHIP_FRICTION

        self.vx, self.vy = clamp_speed(self.vx, self.vy, SHIP_MAX_SPEED)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def wrap(self) -> None:
        """
        Zawijanie statku przez krawędzie ekranu.
        """
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self) -> None:
        """
        Rysuje statek oraz jego kopie przy krawędziach ekranu.
        """
        angle_rad = self.get_angle_rad()

        for draw_x, draw_y in ghost_positions(self.x, self.y, self.radius):
            self._draw_body(draw_x, draw_y, angle_rad)

            if rl.is_key_down(rl.KEY_UP):
                self._draw_engine_flame(draw_x, draw_y, angle_rad)

    def _draw_body(self, draw_x: float, draw_y: float, angle_rad: float) -> None:
        """
        Rysuje obrys statku z linii.

        Dodatkowa żółta kropka na nosie ułatwia sprawdzenie,
        czy pocisk startuje z właściwego miejsca.
        """
        world_points = []

        for local_x, local_y in self.local_points:
            rotated_x, rotated_y = rotate_point(local_x, local_y, angle_rad)
            world_points.append((draw_x + rotated_x, draw_y + rotated_y))

        for index in range(len(world_points)):
            x1, y1 = world_points[index]
            x2, y2 = world_points[(index + 1) % len(world_points)]

            rl.draw_line(int(x1), int(y1), int(x2), int(y2), rl.WHITE)

        nose_x, nose_y = rotate_point(self.radius, 0, angle_rad)
        rl.draw_circle(int(draw_x + nose_x), int(draw_y + nose_y), 2, rl.YELLOW)

    def _draw_engine_flame(self, draw_x: float, draw_y: float, angle_rad: float) -> None:
        """
        Rysuje prosty płomień silnika z tyłu statku.
        """
        flame_left = (-self.radius * 0.75, -5)
        flame_tip = (-self.radius * 1.45, 0)
        flame_right = (-self.radius * 0.75, 5)

        fx1, fy1 = rotate_point(flame_left[0], flame_left[1], angle_rad)
        fx2, fy2 = rotate_point(flame_tip[0], flame_tip[1], angle_rad)
        fx3, fy3 = rotate_point(flame_right[0], flame_right[1], angle_rad)

        rl.draw_line(int(draw_x + fx1), int(draw_y + fy1), int(draw_x + fx2), int(draw_y + fy2), rl.ORANGE)
        rl.draw_line(int(draw_x + fx2), int(draw_y + fy2), int(draw_x + fx3), int(draw_y + fy3), rl.ORANGE)
