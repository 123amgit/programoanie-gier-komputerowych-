# guard.py
# Strażnik biblioteki z prostym patrolem i światłem latarki.

import pyray as pr

from config import GUARD_RADIUS, GUARD_SPEED, FLASHLIGHT_RADIUS
from utils import distance


class Guard:
    def __init__(self, x: float, y: float, patrol_axis: str, patrol_min: float, patrol_max: float) -> None:
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

        self.radius = GUARD_RADIUS
        self.speed = GUARD_SPEED

        self.patrol_axis = patrol_axis
        self.patrol_min = patrol_min
        self.patrol_max = patrol_max
        self.direction = 1

    def update(self, dt: float) -> None:
        if self.patrol_axis == "x":
            self.x += self.direction * self.speed * dt

            if self.x > self.patrol_max:
                self.x = self.patrol_max
                self.direction = -1
            elif self.x < self.patrol_min:
                self.x = self.patrol_min
                self.direction = 1

        elif self.patrol_axis == "y":
            self.y += self.direction * self.speed * dt

            if self.y > self.patrol_max:
                self.y = self.patrol_max
                self.direction = -1
            elif self.y < self.patrol_min:
                self.y = self.patrol_min
                self.direction = 1

    def sees_player(self, player) -> bool:
        return distance(self.x, self.y, player.x, player.y) <= FLASHLIGHT_RADIUS

    def draw_flashlight(self) -> None:
        # Uproszczona latarka jako okrągły obszar światła.
        pr.draw_circle(
            int(self.x),
            int(self.y),
            FLASHLIGHT_RADIUS,
            pr.Color(245, 220, 120, 38),
        )
        pr.draw_circle_lines(
            int(self.x),
            int(self.y),
            FLASHLIGHT_RADIUS,
            pr.Color(245, 220, 120, 105),
        )

    def draw(self) -> None:
        self.draw_flashlight()

        # Ciało strażnika.
        pr.draw_circle(int(self.x), int(self.y), self.radius, pr.Color(95, 120, 165, 255))
        pr.draw_circle_lines(int(self.x), int(self.y), self.radius, pr.Color(180, 205, 240, 255))

        # Czapka / głowa.
        pr.draw_rectangle(
            int(self.x - 12),
            int(self.y - 22),
            24,
            8,
            pr.Color(45, 55, 85, 255),
        )

        # Mała kropka pokazująca kierunek patrolu.
        if self.patrol_axis == "x":
            eye_x = self.x + self.direction * 7
            eye_y = self.y - 2
        else:
            eye_x = self.x
            eye_y = self.y + self.direction * 7

        pr.draw_circle(int(eye_x), int(eye_y), 3, pr.Color(245, 245, 210, 255))
